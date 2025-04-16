from django.urls import path

from . import views_auction
from . import views_user


urlpatterns = [
    path("", views_auction.index, name="index"),                                                            # default view       

    path("login", views_user.login_view, name="login"),                                                     # allow a user to login
    path("logout", views_user.logout_view, name="logout"),                                                  # allow a user to logout        
    path("register", views_user.register, name="register"),                                                 # allow a user to register 

    path("create", views_auction.create, name="create"),                                                    # create a new auction

    path("auctions/<int:auction_id>", views_auction.view, name="view"),                                     # show a specific auction
    path("auctions/<int:auction_id>/bid", views_auction.place_bid, name="place_bid"),                       # place a bid on an auction
    path("auctions/<int:auction_id>/comment", views_auction.add_comment, name="add_comment"),               # add a comment to an auction
    path("auctions/<int:auction_id>/watch", views_auction.toggle_watchlist, name="watch"),                  # add or remove an auction from the watchlist
    path("auctions/<int:auction_id>/close", views_auction.close_auction, name="close_auction"),             # close an auction
]
