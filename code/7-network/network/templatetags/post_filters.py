from django import template
from network.models import Post

register = template.Library()

@register.filter
def is_liked_by(post, user):
    """Check if a post is liked by a specific user"""
    return post.is_liked_by(user)