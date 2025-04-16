from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "start_bid")

class BidAdmin(admin.ModelAdmin):
    list_display = ("auction", "user", "amount")

admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Category, CategoryAdmin)
