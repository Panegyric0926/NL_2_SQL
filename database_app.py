import json
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from call_embedding import (
    get_dense_embedding,
    get_dense_score,
    get_sparse_embedding,
    get_sparse_score
)

DB_FILE = "db.json"
MAX_RECORDS = 100
SCORE_WEIGHT = 0.5

app = FastAPI()


def load_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def _compute_embeddings(item):
    item['Query_Dense'] = get_dense_embedding(item['Query'])
    item['Structure_Dense'] = get_dense_embedding(item['Structure'])
    item['Query_Sparse'] = get_sparse_embedding(item['Query'])
    item['Structure_Sparse'] = get_sparse_embedding(item['Structure'])
    return item


def _sort_and_trim_db(db):
    db.sort(
        key=lambda x: (
            -x.get('Query_Counts', 0),
            datetime.strptime(x.get('Last_Query_Time', "1970-01-01T00:00:00"), "%Y-%m-%dT%H:%M:%S")
        )
    )
    return db[:MAX_RECORDS]


class InsertItem(BaseModel):
    Query: str
    Tables_Involved: str
    Structure: str
    Code: str


class QueryItem(BaseModel):
    Query: str
    Structure: str
    Tables: str


@app.post("/insert")
def insert(item: InsertItem):
    db = load_db()
    record = item.dict()
    record = _compute_embeddings(record)
    record["Query_Counts"] = 1
    record["Last_Query_Time"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    db.append(record)
    db = _sort_and_trim_db(db)
    save_db(db)
    return {"msg": "Inserted", "total": len(db)}


@app.post("/query")
def query(item: QueryItem):
    db = load_db()
    if not db:
        return {"match": False, "msg": "DB is empty."}

    q_dense = get_dense_embedding(item.Query)
    s_dense = get_dense_embedding(item.Structure)
    q_sparse = get_sparse_embedding(item.Query)
    s_sparse = get_sparse_embedding(item.Structure)

    matches = []
    for rec in db:
        if rec.get("Tables_Involved", "") != item.Tables:
            continue

        q_dense_score = get_dense_score(q_dense, rec["Query_Dense"])
        q_sparse_score = get_sparse_score(q_sparse, rec["Query_Sparse"])
        q_final = SCORE_WEIGHT * q_dense_score + (1 - SCORE_WEIGHT) * q_sparse_score

        s_dense_score = get_dense_score(s_dense, rec["Structure_Dense"])
        s_sparse_score = get_sparse_score(s_sparse, rec["Structure_Sparse"])
        s_final = SCORE_WEIGHT * s_dense_score + (1 - SCORE_WEIGHT) * s_sparse_score

        if q_final > 0.95 or s_final > 0.95 or (q_final > 0.5 and s_final > 0.5):
            matches.append((rec, max(q_final, s_final)))

    if not matches:
        return {"match": False, "msg": "No match found."}

    matches.sort(key=lambda x: -x[1])
    best_match = matches[0][0]

    for rec in db:
        if rec == best_match:
            rec["Query_Counts"] += 1
            rec["Last_Query_Time"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            break

    db = _sort_and_trim_db(db)
    save_db(db)

    return {
        "match": True,
        "Code": best_match["Code"],
        "Query_Counts": best_match["Query_Counts"],
        "Last_Query_Time": best_match["Last_Query_Time"]
    }