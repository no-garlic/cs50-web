from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return self.username


class Category(models.Model):
    """
    Category model representing a category for auctions.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Auction(models.Model):
    """
    Auction model representing an auction item.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='auctions')
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')


class Bid(models.Model):
    """
    Bid model representing a bid placed on an auction.
    """
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    winning_bid = models.BooleanField(default=False)


class Comment(models.Model):
    """
    Comment model representing a comment on an auction.
    """
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()


class Watchlist(models.Model):
    """
    Watchlist model representing a user's watchlist for auctions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='watchlists')

