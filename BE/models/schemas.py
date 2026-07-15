from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class TourItemBase(BaseModel):
    contentid: str
    title: Optional[str]
    addr1: Optional[str]
    addr2: Optional[str]
    region: Optional[str]
    content_type: Optional[str]
    firstimage: Optional[str]
    mapx: Optional[float]
    mapy: Optional[float]

class TourItem(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)

class PaginatedTourItems(BaseModel):
    items: List[TourItem]
    limit: int
    offset: int

from datetime import datetime

class PostCreate(BaseModel):
    category: str
    title: str
    content: str
    author: Optional[str] = "익명"
    password: str  # 클라이언트는 원문 비밀번호 전송

class PostOut(BaseModel):
    id: int
    category: str
    title: str
    content: str
    author: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedPosts(BaseModel):
    items: List[PostOut]
    total: int
    limit: int
    offset: int

# models/schemas.py 에 아래 내용 추가

class KnowledgeCreate(BaseModel):
    content: str

class RAGQuery(BaseModel):
    question: str