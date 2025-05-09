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

    # TODO: Handle the error
    if quiz is None:
        return render(request, "quizly/index.html")
    
    return render(request, "quizly/quiz.html", {
        "quiz": quiz,
    })


def attempt(request, quiz_id):
    return render(request, "quizly/attempt.html", {
        "active_filter": "attempt",
    })
