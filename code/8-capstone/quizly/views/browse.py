from django.shortcuts import render
from ..models import *


def index(request):
    return render(request, "quizly/index.html", {
        "active_filter": "index",
    })


def browse(request):
    selected_category_id = request.GET.get("category")
    selected_category = None
    filtered_quizzes = None
    all_categories = []

    if selected_category_id:
        filtered_quizzes = Quiz.objects.filter(category=selected_category_id)
        selected_category = Category.objects.get(id=selected_category_id)
    else:
        all_categories = Category.objects.all()

    return render(request, "quizly/list.html", {
        "active_filter": "browse",
        "all_categories": all_categories,
        "selected_category": selected_category,
        "filtered_quizzes": filtered_quizzes,
    })

