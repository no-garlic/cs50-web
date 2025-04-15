from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from .models import *


class AddAuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'image_url', 'category', 'start_bid']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'image_url': forms.URLInput(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
            'start_bid': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
        }


def index(request):
    all_auctions = Auction.objects.all();
    
    return render(request, "auctions/index.html", {
        "auctions": all_auctions
    })


def view(request, auction_id: int):
    auction = Auction.objects.get(id=auction_id)
    return render(request, "auctions/auction.html", {
        "auction": auction
    })


@login_required
def create(request):
    if request.method == "GET":
        form = AddAuctionForm()    
        return render(request, "auctions/create.html", {
            "auction_form": form
        })
    
    elif request.method == "POST":
        form = AddAuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.owner = request.user
            auction.is_active = True
            auction.save()
            return redirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "auction_form": form
            })


def place_bid(request, auction_id: int):
    pass


def add_comment(request, auction_id: int):
    pass


def toggle_watchlist(request, auction_id: int):
    pass


def close_auction(request, auction_id: int):
    pass
