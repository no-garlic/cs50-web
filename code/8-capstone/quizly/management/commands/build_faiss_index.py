import faiss
import numpy as np
from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
from quizly.models import Quiz
import pickle


class Command(BaseCommand):
    help = "Builds a FAISS index for quiz embeddings"

    def handle(self, *args, **kwargs):
        model = SentenceTransformer('all-MiniLM-L6-v2')

        quizzes = Quiz.objects.all()
        texts = [f"{q.name} {q.description}" for q in quizzes]
        embeddings = model.encode(texts, convert_to_numpy=True)

        for quiz, emb in zip(quizzes, embeddings):
            quiz.embedding = pickle.dumps(emb.astype(np.float32))
            quiz.save()

        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings.astype(np.float32))

        faiss.write_index(index, "faiss_index.idx")
        print("FAISS index built and saved to disk.")
