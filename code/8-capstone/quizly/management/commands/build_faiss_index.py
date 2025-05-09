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

        # Load all quizzes from the database
        quizzes = Quiz.objects.all()

        # Extract the name and description of each quiz
        texts = [f"{q.name} {q.description}" for q in quizzes]

        # Encode the texts into embeddings
        embeddings = model.encode(texts, convert_to_numpy=True).astype(np.float32)

        # Normalize the embeddings for cosine similarity
        faiss.normalize_L2(embeddings)

        # Create a FAISS index for the embeddings
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)

        # Save the index to disk
        faiss.write_index(index, "faiss_index.idx")
        print("FAISS index built and saved to disk.")
