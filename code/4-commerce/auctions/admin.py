from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "start_bid")

class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "user", "amount")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("auction", "user", "content")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("auction", "user")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Category, CategoryAdmin)
