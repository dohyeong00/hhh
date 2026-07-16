from sqlalchemy import select, func
from sqlalchemy.orm import Session
from .models import TourItem

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