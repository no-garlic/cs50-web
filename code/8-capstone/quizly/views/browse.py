from django.shortcuts import render
from ..models import *


def browse(request):
    all_categories = Category.objects.all()

    return render(request, "quizly/list.html", {
        "active_filter": "browse",
        "categories": all_categories
    })

