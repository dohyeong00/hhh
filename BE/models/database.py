from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

ROOT = Path(__file__).resolve().parent.parent
TOUR_DB_PATH = ROOT / "gumi_tourapi.db"
POST_DB_PATH = ROOT / "posts.db"

if not TOUR_DB_PATH.exists():
    TOUR_DB_PATH = ROOT / "DB" / "gumi_tourapi.db"

if not POST_DB_PATH.exists():
    POST_DB_PATH = ROOT / "DB" / "posts.db"

TOUR_SQLALCHEMY_DATABASE_URL = f"sqlite:///{TOUR_DB_PATH}"
POST_SQLALCHEMY_DATABASE_URL = f"sqlite:///{POST_DB_PATH}"

tour_engine = create_engine(
    TOUR_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
post_engine = create_engine(
    POST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TourSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=tour_engine)
PostSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=post_engine)

TourBase = declarative_base()
PostBase = declarative_base()


def get_tour_db():
    db = TourSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_post_db():
    db = PostSessionLocal()
    try:
        yield db
    finally:
        db.close()


# models/database.py 에 아래 내용 추가

RAG_DB_PATH = ROOT / "DB" / "rag_knowledge.db"
RAG_SQLALCHEMY_DATABASE_URL = f"sqlite:///{RAG_DB_PATH}"

rag_engine = create_engine(
    RAG_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
RagSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=rag_engine)
RagBase = declarative_base() # main.py에서 테이블 생성 시 필요

def get_rag_db():
    db_rag = RagSessionLocal()
    try:
        yield db_rag
    finally:
        db_rag.close()

# 기존 ROOT 정의 아래에 추가
ROUTE_DB_PATH = ROOT / "routes.db"
if not ROUTE_DB_PATH.exists():
    ROUTE_DB_PATH = ROOT / "DB" / "routes.db"

ROUTE_SQLALCHEMY_DATABASE_URL = f"sqlite:///{ROUTE_DB_PATH}"

route_engine = create_engine(
    ROUTE_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

RouteSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=route_engine)
RouteBase = declarative_base()

def get_route_db():
    db = RouteSessionLocal()
    try:
        yield db
    finally:
        db.close()