from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username
    
    def get_posts(self):
        return self.posts.all()

    def get_followers(self):
        return self.followers.all()
    
    def get_following(self):
        return self.following.all()
    
    def get_likes(self):
        return self.likes.all()
    
    def get_liked_posts(self):
        return [like.post for like in self.likes.all()]

    def get_followed_users(self):
        return [follow.followed for follow in self.following.all()]
    
    def get_followers_count(self):
        return self.followers.count()
    
    def get_following_count(self):
        return self.following.count()
    
    def get_likes_count(self):
        return self.likes.count()
    
    def get_posts_count(self):
        return self.posts.count()
    
    def get_liked_posts_count(self):
        return len(self.get_liked_posts())
    
    def get_followed_users_count(self):
        return len(self.get_followed_users())
    
    def get_followers_list(self):
        return [follower.follower for follower in self.followers.all()]
    
    def get_following_list(self):
        return [followed.followed for followed in self.following.all()]
    
    def get_likes_list(self):
        return [like.post for like in self.likes.all()]
    
    def get_liked_posts_list(self):
        return [like.post for like in self.likes.all()]
    
    def get_followed_users_list(self):
        return [follow.followed for follow in self.following.all()]
    
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:25]}..."
    

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
    