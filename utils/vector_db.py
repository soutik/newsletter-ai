from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import os

encoder = SentenceTransformer("all-MiniLM-L6-v2")  # Free embeddings

class VectorDB:
    def __init__(self):
        self.client = QdrantClient(url=os.getenv("QDRANT_URL"))
        self.collection_name = "articles"
        self._init_collection()
    
    def _init_collection(self):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
    
    def add_article(self, text):
        embedding = encoder.encode(text).tolist()
        point = PointStruct(
            id=abs(hash(text)),  # Simple hash for dedup, abs to avoid overflow value being negative resulting in vectorDB complaints
            vector=embedding,
            payload={"text": text[:500]}  # Store snippet for validation
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])
    
    def is_duplicate(self, text, user_id):
        embedding = encoder.encode(text).tolist()
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=1,
            score_threshold=0.85  # Similarity threshold
        )
        return len(hits) > 0