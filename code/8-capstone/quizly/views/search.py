import numpy as np
from django.shortcuts import render
from ..services.faiss_search_service import QuizSemanticSearchService
from ..models import *


def search(request):
    """
    Search for quizzes based on a query.
    """
    query = request.GET.get("q")
    search_type = request.GET.get("type")

    if not query or not search_type:
        return render(request, "quizly/list.html", {
            "active_filter": "search",
            "filtered_quizzes": [],
        })

    search_results = []
    
    if search_type == "semantic":
        search_results = semantic_search(query)
    else:
        search_results = keyword_search(query)

    return render(request, "quizly/list.html", {
        "active_filter": "search",
        "filtered_quizzes": search_results,
    })


def keyword_search(query):
    """
    Perform a keyword search on quizzes and categories.
    """
    quizzes = Quiz.objects.filter(name__icontains=query)
    return quizzes


def semantic_search(query):
    """
    Perform a semantic search on quizzes and categories.
    """
    quizzes = list(Quiz.objects.all())
    results = QuizSemanticSearchService.search(query, quizzes, top_k=10)
    return results
