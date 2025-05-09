from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    def __str__(self):
        return self.username
    
    def display_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    

class Category(models.Model):
    """
    Category model representing a category for auctions.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Question(models.Model):
    """
    Question model representing a question in the quiz.
    """
    text = models.TextField()
    hint = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    solution = models.IntegerField(choices=[
        (1, 'Option1'),
        (2, 'Option2'),
        (3, 'Option3'),
        (4, 'Option4'),
    ])
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text
    

class Quiz(models.Model):
    """
    Quiz model representing a quiz.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='quizzes')
    embedding = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class QuizRating(models.Model):
    """
    QuizRating model representing a user's rating for a quiz.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=[
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ])

    def __str__(self):
        return f"{self.user.username} - {self.quiz.name} - {self.rating}"


class QuizAttempt(models.Model):
    """
    QuizAttempt model representing an attempt to take a quiz.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    correct = models.IntegerField()
    score = models.FloatField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"
    

class SavedForLater(models.Model):
    """
    SavedForLater model representing a quiz saved for later by a user.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='saved_for_later')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_for_later')

    def __str__(self):
        return f"{self.user.username} - {self.quiz.name}"
