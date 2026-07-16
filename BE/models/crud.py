from sqlalchemy import select, func
from sqlalchemy.orm import Session
from .models import TourItem
from typing import List

def get_tour_items(db: Session, region: str | None, limit: int, offset: int):
    stmt = select(TourItem).order_by(TourItem.title).limit(limit).offset(offset)
    if region:
        stmt = stmt.where(TourItem.region == region)
    return db.execute(stmt).scalars().all()

def get_place_by_contentid(db: Session, contentid: str):
    stmt = select(TourItem).where(TourItem.contentid == contentid)
    return db.execute(stmt).scalar_one_or_none()

from .models import Post

def create_post(db: Session, payload):
    p = Post(
        category=payload.category,
        title=payload.title,
        content=payload.content,
        author=payload.author or "익명",
        password=payload.password
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def get_posts(db: Session, limit: int = 20, offset: int = 0, category: str | None = None, q: str | None = None):
    stmt = select(Post)
    if category:
        stmt = stmt.where(Post.category == category)
    if q:
        like_q = f"%{q}%"
        stmt = stmt.where(Post.title.ilike(like_q) | Post.content.ilike(like_q) | Post.author.ilike(like_q))
    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    stmt = stmt.order_by(Post.created_at.desc()).limit(limit).offset(offset)
    items = db.scalars(stmt).all()
    return items, total or 0

def get_post(db: Session, post_id: int):
    post = db.get(Post, post_id)
    if post:
        post.views += 1
        db.commit()
        db.refresh(post)
    return post

def verify_password(post: Post, plain: str) -> bool:
    return plain == post.password

def update_post(db: Session, post: Post, title: str, content: str):
    post.title = title
    post.content = content
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post: Post):
    db.delete(post)
    db.commit()

# crud.py 에 아래 내용 추가
import numpy as np
from sqlalchemy import select
from .models import Knowledge

def create_knowledge(db: Session, content: str, embedding_vector: list):
    emb_bytes = np.array(embedding_vector, dtype=np.float32).tobytes()
    k = Knowledge(content=content, embedding=emb_bytes)
    db.add(k)
    db.commit()
    db.refresh(k)
    return k

def get_all_knowledge(db: Session):
    stmt = select(Knowledge)
    return db.scalars(stmt).all()

# models/crud.py 에 추가
import json
from .models import Route
from .schemas import RouteCreate

def create_route(db: Session, payload: RouteCreate):
    # 1. DB 모델 인스턴스 생성
    db_route = Route(
        user_name=payload.user_name,
        title=payload.title,
        # payload.places가 리스트 형태이므로, JSON 문자열로 변환하여 저장
        places_json=json.dumps(payload.places, ensure_ascii=False) 
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    
    # 🌟 [해결 핵심] DB 인스턴스에 임시로 'places' 속성을 달아줍니다.
    # FastAPI가 RouteOut 스키마로 변환할 때 이 'places' 필드를 읽어갑니다.
    db_route.places = payload.places 
    
    return db_route

def get_routes_by_user(db: Session, user_name: str):
    stmt = select(Route).where(Route.user_name == user_name).order_by(Route.created_at.desc())
    routes = db.scalars(stmt).all()
    
    for r in routes:
        # DB에서 가져온 JSON 문자열을 다시 파이썬 리스트로 풀어 r.places에 주입
        r.places = json.loads(r.places_json) if r.places_json else []
    return routes

def get_route_by_id(db: Session, route_id: int):
    route = db.get(Route, route_id)
    if route:
        route.places = json.loads(route.places_json)
    return route

def update_route(db: Session, route: Route, title: str, places: List[str]):
    route.title = title
    route.places_json = json.dumps(places, ensure_ascii=False)
    db.add(route)
    db.commit()
    db.refresh(route)
    route.places = places
    return route

def delete_route(db: Session, route: Route):
    db.delete(route)
    db.commit()