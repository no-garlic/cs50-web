from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from .models import *


class AddAuctionForm(forms.ModelForm):
    """
    Form for creating a new auction.
    It includes fields for title, description, image URL, category, and starting bid.
    """
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
        """
        Initialize the form and set placeholders for each field.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            # Use field's label or capitalize the field name for placeholder
            placeholder_text = field.label if field.label else field_name.replace('_', ' ').capitalize()
            field.widget.attrs['placeholder'] = placeholder_text

            # Remove the label
            field.label = ""


def index(request, error_message=None):
    """
    View function for the index page of the auction site.
    It handles filtering of auctions based on the user's input.

    Parameters:
    - request: The HTTP request object.
    - error_message: Optional error message to display on the page.
    """
    param_listing = request.GET.get("listing")
    param_category = request.GET.get("category")
    active_filter = "active"

    # based on the parameter, we filter the list of auctions that are shown
    if param_listing and param_listing.lower() == "closed":
        # filter by the auctions that are closed
        auctions_query = Auction.objects.filter(is_active=False)
        active_filter = "closed"
    elif param_listing and param_listing.lower() == "my":
        # filter by the auctions that the user has created
        auctions_query = Auction.objects.filter(is_active=True, owner=request.user)
        active_filter = "my"
    elif param_listing and param_listing.lower() == "bids":
        # filter by the auctions that the user has bidded on
        bidded_auctions = Bid.objects.filter(user=request.user).values_list("auction_id", flat=True)
        auctions_query = Auction.objects.filter(is_active=True, id__in=bidded_auctions)
        active_filter = "bids"
    elif param_listing and param_listing.lower() == "watch":
        # filter by the auctions that the user is watching
        watched_auctions = Watchlist.objects.filter(user=request.user).values_list("auction_id", flat=True)
        auctions_query = Auction.objects.filter(is_active=True, id__in=watched_auctions)
        active_filter = "watch"
    elif param_category:
        # filter by the auction category
        category = Category.objects.get(id=param_category)
        auctions_query = Auction.objects.filter(category=category, is_active=True)
        active_filter = category.id
    else:
        # filter by the active auctions
        auctions_query = Auction.objects.filter(is_active=True)        

    # create a list of auctions based on the filter, which we update the value to the highest bid
    auctions_list = list(auctions_query.prefetch_related("bids"))

    # if the user is authenticated, we add the watchlist and bid information to the auction
    if request.user.is_authenticated:
        user_watchlist_ids = set(Watchlist.objects.filter(user=request.user).values_list('auction_id', flat=True))
        for auction in auctions_list:
            auction.is_watched_by_user = auction.id in user_watchlist_ids
            auction.user_is_highest_bidder = auction.is_highest_bidder(request.user)
            auction.user_is_outbid = auction.is_outbid(request.user)
    else:
        # if the user is not authenticated, we set the watchlist and bid information to false
        for auction in auctions_list:
            auction.is_watched_by_user = False
            auction.user_is_highest_bidder = False
            auction.user_is_outbid = False

    # render the index page with the filtered auctions
    return render(request, "auctions/index.html", {
        "auctions": auctions_list,
        "categories": Category.objects.all(),
        "active_filter": active_filter,
        "error_message": error_message
    })


def view(request, auction_id: int, error_message=None):
    """
    View function for displaying a specific auction.
    It handles the display of auction details, bids, comments, and watchlist status.

    Parameters:
    - request: The HTTP request object.
    - auction_id: The ID of the auction to display.
    - error_message: Optional error message to display on the page.
    """
    auction = Auction.objects.get(id=auction_id)
    bids = Bid.objects.filter(auction=auction).order_by('amount')
    comments = Comment.objects.filter(auction=auction).order_by("-id")

    if request.user and request.user.is_authenticated:
        # if the user is authenticated, we check if the user is watching the auction and if they are the highest bidder
        is_watching = Watchlist.objects.filter(auction=auction, user=request.user)
        is_highest_bidder = auction.is_highest_bidder(request.user)
        is_outbid = auction.is_outbid(request.user)
    else:
        # if the user is not authenticated, we set the watchlist and bid information to false
        is_watching = False
        is_highest_bidder = False
        is_outbid = False

    # render the auction page with the auction information, bids, comments, and watchlist information
    return render(request, "auctions/auction.html", {
        "auction": auction,
        "is_watching": is_watching,
        "is_highest_bidder": is_highest_bidder,
        "is_outbid": is_outbid,
        "bids": bids,
        "comments": comments,
        "error_message": error_message,
        "categories": Category.objects.all()
    })


@login_required
def create(request, error_message=None):
    """
    View function for creating a new auction.
    It handles the display of the auction creation form and the submission of the form.

    Parameters:
    - request: The HTTP request object.
    - error_message: Optional error message to display on the page.
    """
    if request.method == "GET":
        # show the auction creation form
        form = AddAuctionForm()    
        return render(request, "auctions/create.html", {
            "auction_form": form,
            "categories": Category.objects.all(),
            "active_filter": "new"
        })
    
    elif request.method == "POST":
        form = AddAuctionForm(request.POST)
        if form.is_valid():
            # save the auction to the database
            auction = form.save(commit=False)
            auction.owner = request.user
            auction.is_active = True
            auction.save()
            return redirect(reverse("index"))
        else:
            # if the form is not valid, show the form again with the error message
            return render(request, "auctions/create.html", {
                "auction_form": form,
                "categories": Category.objects.all(),
                "active_filter": "new",
                "error_message": error_message
            })


@login_required
def place_bid(request):
    """
    View function for placing a bid on an auction.
    It handles the submission of the bid form and the validation of the bid.

    Parameters:
    - request: The HTTP request object.
    """
    if request.method == "POST":
        auction_id = request.POST.get("auction_id")
        amount = request.POST.get("amount")
        auction = Auction.objects.get(id=auction_id)

        if auction != None and amount > auction.current_value() and auction.is_active:
            # check if the user is authenticated and the bid amount is greater than the current value
            user=request.user
            Bid.objects.create(auction=auction, user=user, amount=amount)
            return view(request=request, auction_id=auction_id)
        
    # return the auction page with an error message if the bid is not valid
    return view(request=request, auction_id=-1, error_message="Unable to place the bid")


@login_required
def add_comment(request):
    """
    View function for adding a comment to an auction.
    It handles the submission of the comment form and the validation of the comment.

    Parameters:
    - request: The HTTP request object.
    """
    if request.method == "POST":
        auction_id = request.POST.get("auction_id")
        content = request.POST.get("content")
        auction = Auction.objects.get(id=auction_id)

        if auction != None:
            # check if the user is authenticated and the comment is not empty
            user=request.user
            Comment.objects.create(auction=auction, user=user, content=content)
            return view(request=request, auction_id=auction_id)

    # return the auction page with an error message if the bid is not valid
    return view(request=request, auction_id=-1, error_message="Unable to add the comment")


@login_required
def toggle_watchlist(request):
    """
    View function for adding or removing an auction from the user's watchlist.
    It handles the submission of the watchlist form and the validation of the watchlist.

    Parameters:
    - request: The HTTP request object.
    """
    if request.method == "POST":
        auction_id = request.POST.get("auction_id")
        auction = Auction.objects.get(id=auction_id)

        if auction != None:
            # check if the user is authenticated and the auction is active
            user=request.user
            watched = Watchlist.objects.filter(user=user, auction=auction)
            if watched:
                Watchlist.objects.get(user=user, auction=auction).delete()
            else:
                Watchlist.objects.create(user=user, auction=auction)
            return view(request=request, auction_id=auction_id)

    # return the auction page with an error message if the bid is not valid
    return view(request=request, auction_id=-1, error_message="Unable to toggle the watchlist")


@login_required
def close_auction(request):
    """
    View function for closing an auction.
    It handles the submission of the close auction form and the validation of the auction.

    Parameters:
    - request: The HTTP request object.
    """
    if request.method == "POST":
        auction_id = request.POST.get("auction_id")
        auction = Auction.objects.get(id=auction_id)

        if auction != None and auction.is_active:
            # check if the user is authenticated and the auction is active
            auction.close()
            return view(request=request, auction_id=auction_id)

    # return the auction page with an error message if the bid is not valid
    return view(request=request, auction_id=-1, error_message="Unable to close the auction")
