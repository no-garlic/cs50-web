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
        """
        Lazy load the SentenceTransformer model.
        This ensures that the model is loaded only once and is thread-safe.
        """
        with cls._lock:
            if cls._model is None:
                cls._model = SentenceTransformer('all-MiniLM-L6-v2')
            return cls._model


    @classmethod
    def get_index(cls):
        """
        Lazy load the FAISS index.
        This ensures that the index is loaded only once and is thread-safe.
        """
        with cls._lock:
            if cls._index is None:
                cls._index = faiss.read_index("faiss_index.idx")
            return cls._index


    @classmethod
    def search(cls, query, quizzes, top_k=10, min_similarity=0.3):
        """
        Perform a semantic search on quizzes using FAISS and SentenceTransformer.
        :param query: The search query.
        :param quizzes: List of quizzes to search from.
        :param top_k: Number of top results to return.
        :param min_similarity: Minimum cosine similarity score to consider a quiz as a match.
        :return: List of quizzes that match the query.
        """
        model = cls.get_model()
        index = cls.get_index()

        # Encode the query into an embedding
        query_embedding = model.encode([query], convert_to_numpy=True).astype(np.float32)
        faiss.normalize_L2(query_embedding)

        # Perform the search on the FAISS index
        similarities, indices = index.search(query_embedding, k=top_k)

        print(similarities, indices)

        # Filter results based on the minimum similarity threshold
        results = []
        for i, sim in zip(indices[0], similarities[0]):
            if i < len(quizzes) and sim >= min_similarity:
                results.append((sim, quizzes[i]))

        # Sort results by similarity score in descending order
        results.sort(key=lambda x: x[0], reverse=True)

        # Return only the quizzes, sorted by similarity
        return [quiz for sim, quiz in results]
    