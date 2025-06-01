from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from FlagEmbedding import BGEM3FlagModel
import numpy as np

app = FastAPI()

model = BGEM3FlagModel('bge-m3', use_fp16=True, trust_remote_code=True)

class TextRequest(BaseModel):
    text: str

class TextsRequest(BaseModel):
    texts: List[str]

class EmbeddingRequest(BaseModel):
    embedding1: List[float]
    embedding2: List[float]

class SparseRequest(BaseModel):
    weights1: Dict[str, float]
    weights2: Dict[str, float]

@app.post("/embedding/dense")
def calculate_dense_embedding(req: TextRequest):
    try:
        output = model.encode([req.text], return_dense=True, return_sparse=False, return_colbert_vecs=False)
        dense_vec = output['dense_vecs'][0]
        return {"embedding": dense_vec.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embedding/sparse")
def calculate_sparse_embedding(req: TextRequest):
    try:
        output = model.encode([req.text], return_dense=False, return_sparse=True, return_colbert_vecs=False)
        lex_weights = output['lexical_weights'][0]
        lex_weights = {k: float(v) for k, v in lex_weights.items()}
        return {"sparse_embedding": lex_weights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/score/dense")
def calculate_dense_score(req: EmbeddingRequest):
    try:
        vec1 = np.array(req.embedding1)
        vec2 = np.array(req.embedding2)
        score = float(np.dot(vec1, vec2))
        return {"score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/score/sparse")
def calculate_sparse_score(req: SparseRequest):
    try:
        score = float(model.compute_lexical_matching_score(req.weights1, req.weights2))
        return {"score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"msg": "BGE-M3 Embedding Service. Endpoints: /embedding/dense, /embedding/sparse, /score/dense, /score/sparse"}