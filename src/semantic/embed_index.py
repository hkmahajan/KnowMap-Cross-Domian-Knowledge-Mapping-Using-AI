# src/semantic/embed_index.py
import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

try:
    from sentence_transformers import SentenceTransformer
    MODEL = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    MODEL_AVAILABLE = True
except Exception as e:
    MODEL = None
    MODEL_AVAILABLE = False
    print("⚠️ SentenceTransformer not available:", e)

def build_index(nodes, save_dir="outputs"):
    """Encode node names into vector embeddings."""
    os.makedirs(save_dir, exist_ok=True)
    if not nodes:
        raise ValueError("No nodes provided for embedding.")
    if MODEL_AVAILABLE:
        embeddings = MODEL.encode(nodes, convert_to_numpy=True, show_progress_bar=False)
    else:
        from sklearn.feature_extraction.text import TfidfVectorizer
        vec = TfidfVectorizer().fit(nodes)
        embeddings = vec.transform(nodes).toarray()
    np.save(os.path.join(save_dir, "embeddings.npy"), embeddings)
    json.dump(nodes, open(os.path.join(save_dir, "nodes.json"), "w", encoding="utf-8"))
    return len(nodes), len(embeddings[0])

def load_index(save_dir="outputs"):
    """Load existing embeddings."""
    nodes_path = os.path.join(save_dir, "nodes.json")
    emb_path = os.path.join(save_dir, "embeddings.npy")
    if not os.path.exists(nodes_path) or not os.path.exists(emb_path):
        raise FileNotFoundError("Index files missing.")
    nodes = json.load(open(nodes_path, "r", encoding="utf-8"))
    embeddings = np.load(emb_path, allow_pickle=False)
    return nodes, embeddings

def semantic_search(query, nodes, embeddings, top_k=5):
    """Compute similarity between query and all nodes."""
    if MODEL_AVAILABLE:
        q_vec = MODEL.encode([query], convert_to_numpy=True)
        sims = cosine_similarity(q_vec, embeddings)[0]
    else:
        from sklearn.feature_extraction.text import TfidfVectorizer
        vec = TfidfVectorizer().fit(nodes)
        q_vec = vec.transform([query]).toarray()
        sims = cosine_similarity(q_vec, embeddings)[0]
    idx = np.argsort(sims)[::-1][:top_k]
    return [(nodes[i], float(sims[i])) for i in idx]
