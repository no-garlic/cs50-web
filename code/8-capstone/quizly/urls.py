
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # create a quiz
    path("create", views.create, name="create"),
    
    # show quizzes or categories
    path("browse", views.browse, name="browse"),
    path("search", views.search, name="search"),
    
    # show a users profile
    path("profile/<str:username>", views.profile, name="profile"),

    # show the quiz details
    path("quiz/<int:quiz_id>", views.quiz, name="quiz"),
    
    # attempt a quiz or show the quiz results
    path("attempt/<int:quiz_id>", views.attempt, name="attempt"),

    # account management
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
