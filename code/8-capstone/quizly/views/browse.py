from django.shortcuts import render
from ..models import *


def index(request):
    """
    Show the index page with general information about the application.
    """
    return render(request, "quizly/index.html", {
        "active_filter": "index",
    })


def browse(request):
    """
    Show the list of quizzes filtered by category, or the list of categories.
    """
    # See if there is a category selected
    selected_category_id = request.GET.get("category")
    selected_category = None
    filtered_quizzes = None
    all_categories = []

    # If a category is selected, filter quizzes by that category
    if selected_category_id:
        filtered_quizzes = Quiz.objects.filter(category=selected_category_id)
        selected_category = Category.objects.get(id=selected_category_id)
    else:
        # If no category is selected, show all categories
        all_categories = Category.objects.all()

    # Reder the list page with the filtered quizzes or categories
    return render(request, "quizly/list.html", {
        "active_filter": "browse",
        "all_categories": all_categories,
        "selected_category": selected_category,
        "filtered_quizzes": filtered_quizzes,
    })

