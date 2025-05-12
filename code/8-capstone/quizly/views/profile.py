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


def profile(request, username):
    profile = User.objects.filter(username=username).first()

    active_filter = ""

    if request.user.is_authenticated and request.user.username == username:
        active_filter = "profile"

    return render(request, "quizly/profile.html", {
        "active_filter": active_filter,
        "profile": profile,
    })
