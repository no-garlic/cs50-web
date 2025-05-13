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


def quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)

    if quiz is None:
        return render(request, "quizly/index.html")
    
    user_attempts = []
    user_rating = None
    is_saved_for_later = False
    
    if request.user.is_authenticated:
        user_attempts = quiz.get_attempts_for_user(request.user)
        user_rating = quiz.get_rating_for_user(request.user)
        is_saved_for_later = quiz.get_is_saved_for_later(request.user)
    
    return render(request, "quizly/quiz.html", {
        "quiz": quiz,
        "user_attempts": user_attempts,
        "user_rating": user_rating,
        "is_saved_for_later": is_saved_for_later
    })


def show_attempt(request, quiz_attempt_id):
    quiz_attempt = QuizAttempt.objects.get(id=quiz_attempt_id)
    return render(request, "quizly/attempt.html", {
        "active_filter": "attempt",
        "quiz_attempt": quiz_attempt,
        "answers": quiz_attempt.answers.all(),
        "quiz": quiz_attempt.quiz,
    })
    

@login_required
def new_attempt(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    return render(request, "quizly/attempt.html", {
        "active_filter": "attempt",
        "quiz": quiz,
    })


@login_required
def rate_quiz(request):
    if request.method == "POST":
        quiz_id = request.POST.get("quiz_id")
        rating = request.POST.get("rating")
        quiz = Quiz.objects.get(id=quiz_id)
        user = request.user

        # Check if the user has already rated the quiz
        existing_rating = QuizRating.objects.filter(quiz=quiz, user=user).first()
        if existing_rating:
            existing_rating.rating = rating
            existing_rating.save()
        else:
            new_rating = QuizRating(quiz=quiz, user=user, rating=rating)
            new_rating.save()

        return JsonResponse({"status": "success", "message": "Rating submitted successfully."})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."})
    
    
@login_required
def save_for_later(request):
    if request.method == "POST":
        quiz_id = request.POST.get("quiz_id")
        quiz = Quiz.objects.get(id=quiz_id)
        user = request.user

        # Check if the quiz is already saved for later
        existing_save = SavedForLater.objects.filter(quiz=quiz, user=user).first()
        if existing_save:
            existing_save.delete()
            return JsonResponse({"status": "success", "message": "Quiz removed from saved for later.", "is_saved": False})
        else:
            new_save = SavedForLater(quiz=quiz, user=user)
            new_save.save()
            return JsonResponse({"status": "success", "message": "Quiz saved for later.", "is_saved": True})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."})

