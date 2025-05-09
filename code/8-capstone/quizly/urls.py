
from django.urls import path

from .views.account import *
from .views.other import *

urlpatterns = [
    path("", index, name="index"),

    # create a quiz
    path("create", create, name="create"),
    
    # show quizzes or categories
    path("browse", browse, name="browse"),
    path("search", search, name="search"),
    
    # show a users profile
    path("profile/<str:username>", profile, name="profile"),

    # show the quiz details
    path("quiz/<int:quiz_id>", quiz, name="quiz"),
    
    # attempt a quiz or show the quiz results
    path("attempt/<int:quiz_id>", attempt, name="attempt"),

    # account management
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register, name="register")
]
