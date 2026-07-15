import json
import sqlite3
from pathlib import Path

ROOT = Path(r"c:\Users\SSAFY\Desktop\SSAFY\히히히")
DATA_DIR = ROOT / "data" / "구미_경북권"
DB_PATH = ROOT / "gumi_tourapi.db"

if not DATA_DIR.exists():
    raise SystemExit(f"데이터 폴더를 찾을 수 없습니다: {DATA_DIR}")

# 기존 DB가 있으면 삭제하고 새로 생성
if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE source_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT UNIQUE NOT NULL,
    region TEXT,
    content_type TEXT,
    content_type_id INTEGER,
    total_count INTEGER,
    imported_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tour_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT NOT NULL,
    region TEXT,
    content_type TEXT,
    content_type_id INTEGER,
    contentid TEXT UNIQUE NOT NULL,
    title TEXT,
    addr1 TEXT,
    addr2 TEXT,
    zipcode TEXT,
    tel TEXT,
    mapx REAL,
    mapy REAL,
    mlevel TEXT,
    areacode TEXT,
    sigungucode TEXT,
    lDongRegnCd TEXT,
    lDongSignguCd TEXT,
    cat1 TEXT,
    cat2 TEXT,
    cat3 TEXT,
    lclsSystm1 TEXT,
    lclsSystm2 TEXT,
    lclsSystm3 TEXT,
    firstimage TEXT,
    firstimage2 TEXT,
    cpyrhtDivCd TEXT,
    createdtime TEXT,
    modifiedtime TEXT
);
""")

def parse_float(value):
    try:
        if value in (None, "", " "):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None

json_files = sorted(DATA_DIR.glob("*.json"))

for json_path in json_files:
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    region = data.get("region", "")
    content_type = data.get("contentType", "")
    content_type_id = int(data.get("contentTypeId", 0) or 0)
    items = data.get("items", [])

    cur.execute(
        """
        INSERT INTO source_files (source_file, region, content_type, content_type_id, total_count)
        VALUES (?, ?, ?, ?, ?)
        """,
        (json_path.name, region, content_type, content_type_id, len(items))
    )

    for item in items:
        cur.execute(
            """
            INSERT INTO tour_items (
                source_file, region, content_type, content_type_id, contentid, title, addr1, addr2,
                zipcode, tel, mapx, mapy, mlevel, areacode, sigungucode,
                lDongRegnCd, lDongSignguCd, cat1, cat2, cat3,
                lclsSystm1, lclsSystm2, lclsSystm3,
                firstimage, firstimage2, cpyrhtDivCd, createdtime, modifiedtime
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                json_path.name,
                region,
                content_type,
                content_type_id,
                item.get("contentid", ""),
                item.get("title", ""),
                item.get("addr1", ""),
                item.get("addr2", ""),
                item.get("zipcode", ""),
                item.get("tel", ""),
                parse_float(item.get("mapx")),
                parse_float(item.get("mapy")),
                item.get("mlevel", ""),
                item.get("areacode", ""),
                item.get("sigungucode", ""),
                item.get("lDongRegnCd", ""),
                item.get("lDongSignguCd", ""),
                item.get("cat1", ""),
                item.get("cat2", ""),
                item.get("cat3", ""),
                item.get("lclsSystm1", ""),
                item.get("lclsSystm2", ""),
                item.get("lclsSystm3", ""),
                item.get("firstimage", ""),
                item.get("firstimage2", ""),
                item.get("cpyrhtDivCd", ""),
                item.get("createdtime", ""),
                item.get("modifiedtime", ""),
            ),
        )

conn.commit()
print(f"DB 생성 완료: {DB_PATH}")
print("source_files 테이블 행 수:", cur.execute("SELECT COUNT(*) FROM source_files").fetchone()[0])
print("tour_items 테이블 행 수:", cur.execute("SELECT COUNT(*) FROM tour_items").fetchone()[0])
conn.close()