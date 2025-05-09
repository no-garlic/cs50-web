import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from ..models import *


def search(request):
    query = request.GET.get("q")
    search_type = request.GET.get("type")

    if not query or not search_type:
        return render(request, "quizly/list.html", {
            "active_filter": "search",
            "search_results": [],
        })

    search_results = []
    
    if search_type == "similarity":
        search_results = similarity_search(query)
    else:
        search_results = keyword_search(query)

    return render(request, "quizly/list.html", {
        "active_filter": "search",
        "search_results": search_results,
    })


def keyword_search(query):
    """
    Perform a keyword search on quizzes and categories.
    """
    quizzes = Quiz.objects.filter(name__icontains=query)
    return quizzes


def similarity_search(query):
    """
    Perform a similarity search on quizzes and categories.
    """
    # Placeholder for similarity search logic
    # This could involve using a library like Whoosh or Haystack for full-text search
    return []

