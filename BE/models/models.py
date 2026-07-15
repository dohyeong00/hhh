from sqlalchemy import Column, Float, Integer, String
from .database import TourBase, PostBase

class TourItem(TourBase):
    __tablename__ = "tour_items"

    id = Column(Integer, primary_key=True, index=True)
    source_file = Column(String)
    region = Column(String)
    content_type = Column(String)
    content_type_id = Column(Integer)
    contentid = Column(String, unique=True, index=True)
    title = Column(String)
    addr1 = Column(String)
    addr2 = Column(String)
    zipcode = Column(String)
    tel = Column(String)
    mapx = Column(Float)
    mapy = Column(Float)
    mlevel = Column(String)
    areacode = Column(String)
    sigungucode = Column(String)
    lDongRegnCd = Column(String)
    lDongSignguCd = Column(String)
    cat1 = Column(String)
    cat2 = Column(String)
    cat3 = Column(String)
    lclsSystm1 = Column(String)
    lclsSystm2 = Column(String)
    lclsSystm3 = Column(String)
    firstimage = Column(String)
    firstimage2 = Column(String)
    cpyrhtDivCd = Column(String)
    createdtime = Column(String)
    modifiedtime = Column(String)

from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

class Post(PostBase):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String, default="익명")
    password = Column(String, nullable=False)  # 평문 저장 (교육용)
    created_at = Column(DateTime, default=datetime.utcnow)