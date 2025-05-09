import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import threading

class QuizSemanticSearchService:
    _model = None
    _index = None
    _lock = threading.Lock()

    @classmethod
    def get_model(cls):
        with cls._lock:
            if cls._model is None:
                cls._model = SentenceTransformer('all-MiniLM-L6-v2')
            return cls._model

    @classmethod
    def get_index(cls):
        with cls._lock:
            if cls._index is None:
                cls._index = faiss.read_index("faiss_index.idx")
            return cls._index

    @classmethod
    def search(cls, query, quizzes, top_k=10):
        model = cls.get_model()
        index = cls.get_index()

        query_embedding = model.encode([query], convert_to_numpy=True).astype(np.float32)
        D, I = index.search(query_embedding, k=top_k)

        print(I)
        print(D)

        results = []

        for n in range(len(I[0])):
            d = D[0][n]
            i = I[0][n]

            if i < len(quizzes) and d < 1.5:
                results.append(quizzes[i])

        return results
