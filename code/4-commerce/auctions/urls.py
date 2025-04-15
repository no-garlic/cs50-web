from django.urls import path

from . import views_auction
from . import views_category
from . import views_search
from . import views_user
from . import views_watchlist


urlpatterns = [
    path("", views_user.index, name="index"),                                                               # default view          
    path("login", views_user.login_view, name="login"),                                                     # allow a user to login
    path("logout", views_user.logout_view, name="logout"),                                                  # allow a user to logout        
    path("register", views_user.register, name="register"),                                                 # allow a user to register 

    path("create_auction", views_auction.create_auction, name="create_auction"),                            # create a new auction

    path("auctions/<int:auction_id>", views_auction.view_auction, name="view_auction"),                     # show a specific auction
    path("auctions/<int:auction_id>/bid", views_auction.place_bid, name="place_bid"),                       # place a bid on an auction
    path("auctions/<int:auction_id>/comment", views_auction.add_comment, name="add_comment"),               # add a comment to an auction
    path("auctions/<int:auction_id>/watchlist", views_auction.toggle_watchlist, name="toggle_watchlist"),   # add or remove an auction from the watchlist
    path("auctions/<int:auction_id>/close", views_auction.close_auction, name="close_auction"),             # close an auction
    path("auctions/<int:auction_id>/edit", views_auction.edit_auction, name="edit_auction"),                # edit an auction
    path("auctions/<int:auction_id>/delete", views_auction.delete_auction, name="delete_auction"),          # delete an auction

    path("watchlist", views_watchlist.watchlist, name="watchlist"),                                         # show all auctions in the users watchlist              
    
    path("categories", views_category.categories, name="categories"),                                       # show all categories
    path("categories/<str:category_name>", views_category.category_auctions, name="category_auctions"),     # show all auctions for a specific category
    
    path("search", views_search.search, name="search"),                                                     # search for auctions by title or description
    path("search/<str:query>", views_search.search_results, name="search_results"),                         # show search results for a specific query
]
