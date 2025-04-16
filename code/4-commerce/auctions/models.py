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

    def __str__(self):
        return f"{self.title} @ {self.owner.username}"

    def highest_bid(self):
        bid = Bid.objects.filter(auction=self).order_by('amount').first()
        return bid

    def highest_bid_for_user(self, user):
        bid = Bid.objects.filter(auction=self, user=user).order_by('amount').first()
        return bid

    def is_highest_bidder(self, user):
        bid = self.highest_bid()
        return bid and bid.user == user

    def is_outbid(self, user):
        user_bid = self.highest_bid_for_user(user)
        if user_bid:
            highest_bid = self.highest_bid()
            return highest_bid != user_bid
        return False


class Bid(models.Model):
    """
    Bid model representing a bid placed on an auction.
    """
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    winning_bid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.auction} - bid: {self.amount} @ {self.user.username}"


class Comment(models.Model):
    """
    Comment model representing a comment on an auction.
    """
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    def __str__(self):
        return f"{self.auction.title} ({self.user.username}): {self.content}"


class Watchlist(models.Model):
    """
    Watchlist model representing a user's watchlist for auctions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='watchlists')

