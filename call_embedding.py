import requests

base_url = 'http://localhost:8000'

def get_dense_embedding(text):
    resp = requests.post(f"{base_url}/embedding/dense", json={'text': text})
    return resp.json()['embedding']

def get_sparse_embedding(text):
    resp = requests.post(f"{base_url}/embedding/sparse", json={'text': text})
    return resp.json()['sparse_embedding']

def get_dense_score(emb1, emb2):
    resp = requests.post(f"{base_url}/score/dense", json={'embedding1': emb1, 'embedding2': emb2})
    return resp.json()['score']

def get_sparse_score(w1, w2):
    resp = requests.post(f"{base_url}/score/sparse", json={'weights1': w1, 'weights2': w2})
    return resp.json()['score']

if __name__ == "__main__":
    text1 = "What is BGE M3?"
    text2 = "BGE M3 is an embedding model supporting dense retrieval, lexical matching and multi-vector interaction."
    
    emb1 = get_dense_embedding(text1)
    emb2 = get_dense_embedding(text2)
    print("[Dense] Embedding 1:", emb1[:5], "...")
    print("[Dense] Embedding 2:", emb2[:5], "...")

    dense_score = get_dense_score(emb1, emb2)
    print("[Dense] Score:", dense_score)
    
    sparse1 = get_sparse_embedding(text1)
    sparse2 = get_sparse_embedding(text2)
    print("[Sparse] Weights 1:", sparse1)
    print("[Sparse] Weights 2:", sparse2)
    
    sparse_score = get_sparse_score(sparse1, sparse2)
    print("[Sparse] Score:", sparse_score)