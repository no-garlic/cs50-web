from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


def create_auction(request):
    pass


def view_auction(request, auction_id: int):
    pass


def place_bid(request, auction_id: int):
    pass


def add_comment(request, auction_id: int):
    pass


def toggle_watchlist(request, auction_id: int):
    pass


def close_auction(request, auction_id: int):
    pass


def edit_auction(request, auction_id: int):
    pass


def delete_auction(request, auction_id: int):
    pass
