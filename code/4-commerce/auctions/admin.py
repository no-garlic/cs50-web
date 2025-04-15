from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(User, UserAdmin)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Category, CategoryAdmin)
