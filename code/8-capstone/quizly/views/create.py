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


@login_required
def create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)

        # TODO: Create the embedding
        embedding = None

        # Create the quiz
        quiz = Quiz.objects.create(
            name=name,
            description=description,
            category=category,
            created_by=request.user,
            embedding=embedding,
        )

        return redirect("quiz", quiz_id=quiz.id)

    else:
        categories = Category.objects.all()
        return render(request, "quizly/create.html", {
            "active_filter": "create",
            "categories": categories,
        })

