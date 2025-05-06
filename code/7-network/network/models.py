from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username
    
    def display_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    
    def is_following(self, user):
        return self.following.filter(followed=user).exists()
    
        
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:25]}..."
    
    def get_likes_count(self):
        return self.likes.count()
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user.username} likes post: {self.post.content[:25]}..."
    

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.follower.username} is following: {self.followed.username}"
    