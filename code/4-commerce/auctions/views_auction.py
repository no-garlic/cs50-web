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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Use field's label or capitalize the field name for placeholder
            placeholder_text = field.label if field.label else field_name.replace('_', ' ').capitalize()
            field.widget.attrs['placeholder'] = placeholder_text
            # Remove the label
            field.label = ""


def index(request):
    param_listing = request.GET.get("listing")
    param_category = request.GET.get("category")
    active_filter = "active"

    if param_listing and param_listing.lower() == "closed":
        auctions_query = Auction.objects.filter(is_active=False)
        active_filter = "closed"
    elif param_listing and param_listing.lower() == "my":
        auctions_query = Auction.objects.filter(is_active=True, owner=request.user)
        active_filter = "my"
    elif param_listing and param_listing.lower() == "bids":
        bidded_auctions = Bid.objects.filter(user=request.user).values_list("auction_id", flat=True)
        auctions_query = Auction.objects.filter(is_active=True, id__in=bidded_auctions)
        active_filter = "bids"
    elif param_listing and param_listing.lower() == "watch":
        watched_auctions = Watchlist.objects.filter(user=request.user).values_list("auction_id", flat=True)
        auctions_query = Auction.objects.filter(is_active=True, id__in=watched_auctions)
        active_filter = "watch"
    elif param_category:
        try:
            category = Category.objects.get(id=param_category)
            auctions_query = Auction.objects.filter(category=category, is_active=True)
            active_filter = category.id
        except Category.DoesNotExist:
            auctions_query = Auction.objects.none()            
        except ValueError:  
            auctions_query = Auction.objects.filter(is_active=True)           
    else:
        auctions_query = Auction.objects.filter(is_active=True)        

    auctions_list = list(auctions_query.prefetch_related("bids"))

    if request.user.is_authenticated:
        user_watchlist_ids = set(Watchlist.objects.filter(user=request.user).values_list('auction_id', flat=True))
        for auction in auctions_list:
            auction.is_watched_by_user = auction.id in user_watchlist_ids
            auction.user_is_highest_bidder = auction.is_highest_bidder(request.user)
            auction.user_is_outbid = auction.is_outbid(request.user)
    else:
        for auction in auctions_list:
            auction.is_watched_by_user = False
            auction.user_is_highest_bidder = False
            auction.user_is_outbid = False

    return render(request, "auctions/index.html", {
        "auctions": auctions_list,
        "categories": Category.objects.all(),
        "active_filter": active_filter
    })


def view(request, auction_id: int):
    auction = Auction.objects.get(id=auction_id)
    bids = Bid.objects.filter(auction=auction).order_by('amount')
    comments = Comment.objects.filter(auction=auction).order_by("-id")

    if request.user and request.user.is_authenticated:
        is_watching = Watchlist.objects.filter(auction=auction, user=request.user)
        is_highest_bidder = auction.is_highest_bidder(request.user)
        is_outbid = auction.is_outbid(request.user)
    else:
        is_watching = False
        is_highest_bidder = False
        is_outbid = False

    return render(request, "auctions/auction.html", {
        "auction": auction,
        "is_watching": is_watching,
        "is_highest_bidder": is_highest_bidder,
        "is_outbid": is_outbid,
        "bids": bids,
        "comments": comments,
        "categories": Category.objects.all()
    })


@login_required
def create(request):
    if request.method == "GET":
        form = AddAuctionForm()    
        return render(request, "auctions/create.html", {
            "auction_form": form,
            "categories": Category.objects.all(),
            "active_filter": "new"
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
                "auction_form": form,
                "categories": Category.objects.all(),
                "active_filter": "new"
            })


# TODO:
#
#   Watch Item Toggle
#   Add Comment
#   Place Bid
#   Close Auction
#   Admin View


def place_bid(request):
    pass


def add_comment(request):
    if request.method == "POST":
        auction_id = request.POST.get("auction_id")
        content = request.POST.get("content")
        auction = Auction.objects.get(id=auction_id)
        user=request.user
        Comment.objects.create(auction=auction, user=user, content=content)
        return view(request=request, auction_id=auction_id)
    else:
        #error
        pass

def toggle_watchlist(request):
    pass


def close_auction(request):
    pass
