# main.py 상단 import 추가
import os
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from .models.database import RagBase, rag_engine, get_rag_db
from .models.schemas import KnowledgeCreate, RAGQuery
from .models.crud import create_knowledge, get_all_knowledge

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

# 개발용: 필요한 origin만 허용하세요. '*'는 개발 전용입니다.
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

TourBase.metadata.create_all(bind=tour_engine)
PostBase.metadata.create_all(bind=post_engine)

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
    allow_origins=origins,       # 또는 ["*"] (개발 전용)
    allow_credentials=True,
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
                "imageUrl": it.firstimage or it.firstimage2 or "",
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
                "imageUrl": it.firstimage or it.firstimage2 or "",
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
    db: Session = Depends(get_post_db),
):
    items, total = get_posts(db, limit=limit, offset=offset, category=category, q=q)
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


@app.post("/rag/query")
def query_rag(payload: RAGQuery, db: Session = Depends(get_tour_db)):
    # payload.query 예: "구미 금오산 근처 맛집 추천해줘"
    query_text = payload.question.strip()
    
    # [핵심] 임베딩 벡터 검색 대신, 간단한 키워드 필터링을 수행합니다.
    # 사용자가 입력한 단어 중 주요 키워드를 뽑아서 DB에서 관련 항목들을 가져옵니다.
    words = [w for w in query_text.split() if len(w) > 1] # 2글자 이상 단어 추출
    
    if words:
        # 단어들 중 하나라도 포함하는 관광 아이템 조회
        conditions = [TourItem.title.ilike(f"%{word}%") | TourItem.addr1.ilike(f"%{word}%") for word in words]
        stmt = select(TourItem).where(or_(*conditions)).limit(5)
    else:
        stmt = select(TourItem).limit(5)
        
    items = db.scalars(stmt).all()
    
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