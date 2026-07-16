# main.py 상단 import 추가
import os
import re
import json
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from .models.database import RagBase, rag_engine, get_rag_db, RouteBase, route_engine, get_route_db
from .models.schemas import KnowledgeCreate, RAGQuery, RouteCreate, RouteOut
from .models.crud import create_knowledge, get_all_knowledge, create_route, get_routes_by_user, get_route_by_id, update_route, delete_route

from fastapi import Body, Depends, FastAPI, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from .models.database import (
    TourBase,
    PostBase,
    tour_engine,
    post_engine,
    get_tour_db,
    get_post_db,
)
from .models.models import TourItem
from .models.schemas import PaginatedTourItems, TourItem as TourItemSchema

from .models.crud import (
    create_post,
    get_posts,
    get_post,
    verify_password,
    update_post,
    delete_post,
)
from .models.schemas import PostCreate, PostOut, PaginatedPosts
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

TourBase.metadata.create_all(bind=tour_engine)
PostBase.metadata.create_all(bind=post_engine)
RouteBase.metadata.create_all(bind=route_engine)

# RAG 테이블 생성 등록
RagBase.metadata.create_all(bind=rag_engine)

app = FastAPI(
    title="Gumi Tour API",
    version="0.1.0",
    docs_url="/swagger",
    redoc_url=None,
    openapi_url="/openapi.json",
    swagger_ui_parameters={"displayRequestDuration": True},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=False, # 중복 허용 불가하므로 False 설정
    allow_methods=["*"],
    allow_headers=["*"],
)

CATEGORY_OPTIONS = ["관광지", "숙박", "음식점", "쇼핑", "레포츠"]
CATEGORY_ALIASES = {
    "관광지": ["관광지", "tourist", "tour"],
    "숙박": ["숙박", "accommodation", "hotel"],
    "음식점": ["음식점", "restaurant", "food"],
    "쇼핑": ["쇼핑", "shopping", "shop"],
    "레포츠": ["레포츠", "leports", "sports"],
}
CATEGORY_TO_CONTENT_TYPE_ID = {
    "관광지": 12,
    "숙박": 32,
    "음식점": 39,
    "쇼핑": 38,
    "레포츠": 28,
}

# 🌟 사진이 없을 때 사용할 기본 아이콘/이미지 매핑 추가
DEFAULT_ICON = "https://images.unsplash.com/photo-1488646953014-85cb44e25828?q=80&w=300&auto=format&fit=crop" # 공통 기본 (나침반/여행지도 이미지 등)
CATEGORY_ICONS = {
    "관광지": "https://cdn-icons-png.flaticon.com/512/854/854829.png",    # 관광지 아이콘
    "숙박": "https://cdn-icons-png.flaticon.com/512/2983/2983803.png",     # 숙박/호텔 아이콘
    "음식점": "https://cdn-icons-png.flaticon.com/512/1046/1046747.png",   # 음식점/식사 아이콘
    "쇼핑": "https://cdn-icons-png.flaticon.com/512/1170/1170678.png",     # 쇼핑/카트 아이콘
    "레포츠": "https://cdn-icons-png.flaticon.com/512/3144/3144933.png",   # 스포츠/액티비티 아이콘
}


def normalize_category(value: str | None) -> str | None:
    if not value:
        return None

    raw = value.strip()
    if not raw:
        return None

    lowered = raw.lower()
    for category in CATEGORY_OPTIONS:
        if category.lower() == lowered:
            return category

    for category in CATEGORY_OPTIONS:
        if any(alias.lower() == lowered for alias in CATEGORY_ALIASES[category]):
            return category

    return None


def normalize_categories(values: list[str] | None) -> list[str]:
    if not values:
        return []

    result: list[str] = []
    for value in values:
        if not value:
            continue
        for part in str(value).split(","):
            cleaned = part.strip()
            if not cleaned:
                continue
            normalized = normalize_category(cleaned)
            if normalized and normalized not in result:
                result.append(normalized)
    return result

# OpenAI 클라이언트 초기화
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)  
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

@app.get("/")
def read_root():
    return {"message": "Gumi Tour API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/tour-items", response_model=PaginatedTourItems, tags=["tour"])
def list_tour_items(
    region: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_tour_db),
):
    stmt = select(TourItem)
    if region:
        stmt = stmt.where(TourItem.region == region)

    stmt = stmt.order_by(TourItem.title).limit(limit).offset(offset)
    items = db.scalars(stmt).all()

    return {
        "items": [TourItemSchema.from_orm(item) for item in items],
        "limit": limit,
        "offset": offset,
    }


@app.get("/places/categories", tags=["places"], summary="List available categories")
def list_place_categories():
    return {"categories": CATEGORY_OPTIONS}


@app.get(
    "/places/all",
    tags=["places"],
    summary="Get all places",
    description="Retrieve all places from the database in the search result format without pagination.",
)
def get_all_places(db: Session = Depends(get_tour_db)):
    # 1. 전체 데이터 조회 (정렬 기준은 이름순)
    stmt = select(TourItem).order_by(TourItem.title)
    items = db.scalars(stmt).all()
    total = len(items)

    # 2. 결과 가공을 위한 매핑 정보 (기존 search_places와 동일)
    CITY_NAME_MAP = {
        "Gyeongju": "경주시",
        "Andong": "안동시",
        "Pohang": "포항시",
        "Gumi": "구미시",
        "Uljin": "울진군",
    }

    def normalize_cat_for_output(ct):
        if not ct:
            return ""
        nc = normalize_category(ct)
        return nc if nc else str(ct)

    # 3. 데이터 변환 및 포맷팅
    result_items = []
    for it in items:
        cat = normalize_cat_for_output(it.content_type)
        
        # 🌟 사진 예외 처리 로직 적용
        original_image = it.firstimage or it.firstimage2 or ""
        # 원본 이미지가 없거나 공백 문자열인 경우 대체 아이콘 설정
        if not original_image.strip():
            image_url = CATEGORY_ICONS.get(cat, DEFAULT_ICON)
        else:
            image_url = original_image

        result_items.append(
            {
                "id": it.contentid or f"db-{it.id}",
                "city": it.region or "",
                "cityName": CITY_NAME_MAP.get(it.region, it.region or ""),
                "name": it.title or "",
                "lat": float(it.mapy) if it.mapy is not None else None,
                "lng": float(it.mapx) if it.mapx is not None else None,
                "category": cat,
                "desc": it.addr1 or it.addr2 or "",
                "imageUrl": image_url,  # 👈 수정된 이미지 URL 주입
            }
        )

    # 4. /places/search와 완벽히 호환되는 구조로 반환
    return {
        "items": result_items,
        "total": total,
        "limit": total,       # 전체 데이터이므로 limit은 전체 개수로 설정
        "offset": 0,          # 페이징이 없으므로 시작점은 0
        "selected_categories": [], # 필터가 없으므로 빈 배열 반환
    }


@app.get(
    "/places/search",
    tags=["places"],
    summary="Search places",
    description="Search places by keyword and filter by category",
)
def search_places(
    q: str | None = Query(default=None, min_length=1),
    region: str | None = Query(default=None),
    category: str | None = Query(default=None),
    categories: list[str] | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_tour_db),
):
    filters = []

    if q:
        like_q = f"%{q}%"
        filters.append(
            TourItem.title.ilike(like_q)
        )

    if region:
        filters.append(TourItem.addr1.ilike(f"%{region}%") | TourItem.addr2.ilike(f"%{region}%"))

    selected_categories = normalize_categories([category] if category else []) + normalize_categories(
        categories
    )
    if selected_categories:
        category_clauses = []
        for selected in selected_categories:
            category_clauses.append(
                or_(
                    func.lower(func.coalesce(TourItem.content_type, "")).like(f"%{selected.lower()}%"),
                    TourItem.content_type_id == CATEGORY_TO_CONTENT_TYPE_ID[selected],
                )
            )
        filters.append(or_(*category_clauses))

    count_stmt = select(func.count()).select_from(TourItem)
    if filters:
        count_stmt = count_stmt.where(*filters)
    total = db.scalar(count_stmt) or 0

    stmt = select(TourItem)
    if filters:
        stmt = stmt.where(*filters)
    stmt = stmt.order_by(TourItem.title).limit(limit).offset(offset)

    items = db.scalars(stmt).all()

    CITY_NAME_MAP = {
        "Gyeongju": "경주시",
        "Andong": "안동시",
        "Pohang": "포항시",
        "Gumi": "구미시",
        "Uljin": "울진군",
    }

    def normalize_cat_for_output(ct):
        if not ct:
            return ""
        nc = normalize_category(ct)
        return nc if nc else str(ct)

    result_items = []
    for it in items:
        cat = normalize_cat_for_output(it.content_type)
        
        # 🌟 사진 예외 처리 로직 적용
        original_image = it.firstimage or it.firstimage2 or ""
        # 원본 이미지가 없거나 공백 문자열인 경우 대체 아이콘 설정
        if not original_image.strip():
            image_url = CATEGORY_ICONS.get(cat, DEFAULT_ICON)
        else:
            image_url = original_image

        result_items.append(
            {
                "id": it.contentid or f"db-{it.id}",
                "city": it.region or "",
                "cityName": CITY_NAME_MAP.get(it.region, it.region or ""),
                "name": it.title or "",
                "lat": float(it.mapy) if it.mapy is not None else None,
                "lng": float(it.mapx) if it.mapx is not None else None,
                "category": cat,
                "desc": it.addr1 or it.addr2 or "",
                "imageUrl": image_url,  # 👈 수정된 이미지 URL 주입
            }
        )

    return {
        "items": result_items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "selected_categories": selected_categories,
    }


@app.get("/places/{contentid}", tags=["places"], summary="Get place detail", response_model=TourItemSchema)
def get_place_detail(contentid: str, db: Session = Depends(get_tour_db)):
    stmt = select(TourItem).where(TourItem.contentid == contentid)
    item = db.scalar(stmt)
    if item is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return item


@app.post("/posts", response_model=PostOut, tags=["posts"])
def api_create_post(payload: PostCreate, db: Session = Depends(get_post_db)):
    return create_post(db, payload)


@app.get("/posts", response_model=PaginatedPosts, tags=["posts"])
def api_list_posts(
    limit: int = 20,
    offset: int = 0,
    category: str | None = None,
    q: str | None = None,
    sort: str = Query(default="created_at", description="정렬 기준 (created_at: 최신순, views: 인기순)"), # 👈 쿼리 파라미터 추가
    db: Session = Depends(get_post_db),
):
    # crud의 get_posts 호출 시 sort_by 매개변수로 넘겨줌
    items, total = get_posts(db, limit=limit, offset=offset, category=category, q=q, sort_by=sort)
    return {"items": [PostOut.from_orm(i) for i in items], "total": total, "limit": limit, "offset": offset}


@app.get("/posts/{post_id}", response_model=PostOut, tags=["posts"])
def api_get_post(post_id: int, db: Session = Depends(get_post_db)):
    p = get_post(db, post_id)
    if not p:
        raise HTTPException(status_code=404, detail="Post not found")
    return p


class PasswordBody(BaseModel):
    password: str


@app.put("/posts/{post_id}", response_model=PostOut, tags=["posts"])
def api_update_post(
    post_id: int,
    body: PostCreate | None = Body(None),
    password_body: PasswordBody = Body(...),
    db: Session = Depends(get_post_db),
):
    p = get_post(db, post_id)
    if not p:
        raise HTTPException(404, "Not found")
    if not verify_password(p, password_body.password):
        raise HTTPException(401, "Invalid password")
    return update_post(db, p, title=body.title, content=body.content)


@app.delete("/posts/{post_id}", tags=["posts"])
def api_delete_post(
    post_id: int,
    password_body: PasswordBody = Body(...),
    db: Session = Depends(get_post_db),
):
    p = get_post(db, post_id)
    if not p:
        raise HTTPException(404, "Not found")
    if not verify_password(p, password_body.password):
        raise HTTPException(401, "Invalid password")
    delete_post(db, p)
    return {"detail": "deleted"}


@app.post("/rag/query", tags=["GPT"], summary="Query RAG knowledge base")
def query_rag(payload: RAGQuery, db: Session = Depends(get_tour_db)):
    # payload.query 예: "구미 금오산 근처 맛집 추천해줘"
    query_text = payload.question.strip()
    
    if query_text:
        # 공백 기준으로 단어 분리 (간단 처리)
        words = [w.strip() for w in re.split(r"\s+", query_text) if len(w.strip()) > 0]
        if words:
            patterns = [f"%{w}%" for w in words]
            # 각 단어에 대해 (title OR addr1 OR addr2) 조건 생성
            per_word_clauses = [
                or_(
                    TourItem.title.ilike(p),
                    TourItem.addr1.ilike(p),
                    TourItem.addr2.ilike(p),
                    TourItem.content_type.ilike(p),
                )
                for p in patterns
            ]
            # 모든 단어 조건을 AND로 결합 (where(*clauses)는 AND 효과)
            stmt = select(TourItem).where(*per_word_clauses).order_by(TourItem.title).limit(5).offset(0)
        else:
            stmt = select(TourItem).order_by(TourItem.title).limit(5).offset(0)
    else:
        stmt = select(TourItem).order_by(TourItem.title).limit(5).offset(0)
        
    items = db.scalars(stmt).all()
    print(f"RAG Query: '{query_text}' -> Retrieved {len(items)} items from DB")
    
    # 4. 조회된 데이터를 텍스트 컨텍스트로 구성
    context_parts = []
    for idx, item in enumerate(items, 1):
        context_parts.append(
            f"[{idx}] 이름: {item.title}\n"
            f"   - 카테고리: {item.content_type or '미지정'}\n"
            f"   - 주소: {item.addr1 or ''} {item.addr2 or ''}\n"
            f"   - 전화번호: {item.tel or '없음'}"
        )
    retrieved_context = "\n\n".join(context_parts)
    
    # 5. gpt-5-mini에 전달할 프롬프트 구성
    if items:
        system_prompt = f"""너는 구미 및 경북 지역 관광 전문 안내 비서야.
반드시 제공된 [관광 데이터 목록]에 존재하는 실제 관광지만을 추천하고 설명해야 해.
목록에 없는 관광지를 억지로 지어내서 추천하지 마. 답변할 때 구체적인 주소와 전화번호가 있다면 함께 친절하게 안내해줘.

[관광 데이터 목록]
{retrieved_context}"""
    else:
        system_prompt = """너는 구미 및 경북 지역 관광 전문 안내 비서야.
현재 사용자가 찾는 조건에 맞는 관광 데이터가 DB에 없어. 
정중하게 사과하고, 어떤 지역의 정보를 찾으시는지 구체적으로 다시 물어봐줘."""

    # 6. gpt-5-mini 호출
    response = openai_client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query_text}
        ]
    )
    
    return {"answer": response.choices[0].message.content}

# 1. 여행 코스 저장 API
# API 엔드포인트 등록 시 get_route_db 사용
@app.post("/routes", response_model=RouteOut, tags=["routes"])
def save_user_route(payload: RouteCreate, db: Session = Depends(get_route_db)):
    return create_route(db, payload)

# 2. 특정 사용자의 모든 여행 코스 불러오기 API
@app.get("/routes/user/{user_name}", response_model=list[RouteOut], tags=["routes"])
def load_user_routes(user_name: str, db: Session = Depends(get_route_db)):
    return get_routes_by_user(db, user_name)

# 3. 여행 코스 수정 API
@app.put("/routes/{route_id}", response_model=RouteOut, tags=["routes"])
def modify_route(route_id: int, title: str, places: list[str], db: Session = Depends(get_route_db)):
    db_route = get_route_by_id(db, route_id)
    if not db_route:
        raise HTTPException(status_code=404, detail="해당 코스를 찾을 수 없습니다.")
    return update_route(db, db_route, title, places)

@app.delete("/routes/{route_id}", tags=["routes"])
def delete_user_route(route_id: int, db: Session = Depends(get_route_db)):
    # 1. 삭제할 코스가 존재하는지 조회
    db_route = get_route_by_id(db, route_id)
    if not db_route:
        raise HTTPException(status_code=404, detail="해당 여행 코스를 찾을 수 없습니다.")
    
    # 2. 존재하면 DB에서 삭제 수행
    delete_route(db, db_route)
    
    # 3. 삭제 성공 메시지 반환
    return {"message": f"ID {route_id}번 여행 코스가 성공적으로 삭제되었습니다."}