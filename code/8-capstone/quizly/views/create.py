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
        form_action = request.POST.get("form_action")

        if form_action == "save_quiz":
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

            return render(request, "quizly/create.html", {
                "active_filter": "create",
                "quiz": quiz,
            })
        
        elif form_action == "save_question":
            quiz_id = request.POST.get("quiz_id")
            quiz = Quiz.objects.get(id=quiz_id)

            question_text = request.POST.get("question_text")
            hint = request.POST.get("hint")
            option1 = request.POST.get("option1")
            option2 = request.POST.get("option2")
            option3 = request.POST.get("option3")
            option4 = request.POST.get("option4")
            solution = int(request.POST.get("solution"))

            print(request.POST)


            # Create the question
            Question.objects.create(
                text=question_text,
                hint=hint,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                solution=solution,
                quiz=quiz,
            )

            return render(request, "quizly/create.html", {
                "active_filter": "create",
                "quiz": quiz,
            })

        #return redirect("quiz", quiz_id=quiz.id)

    else:
        categories = Category.objects.all()
        return render(request, "quizly/create.html", {
            "active_filter": "create",
            "categories": categories,
        })

