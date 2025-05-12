from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    def __str__(self):
        return self.username
    
    def display_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    
    def get_saved_for_later(self):
        """
        Get the quizzes saved for later by the user.
        """
        saved_quiz_ids = SavedForLater.objects.filter(user=self).values_list('quiz', flat=True)
        return Quiz.objects.filter(id__in=saved_quiz_ids)

    def get_completed_quizzes(self):
        """
        Get the quizzes completed by the user.
        """
        completed_quiz_ids = QuizAttempt.objects.filter(user=self).values_list('quiz', flat=True).distinct()
        return Quiz.objects.filter(id__in=completed_quiz_ids)
        

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
    
    def get_average_rating(self):
        """
        Calculate the average rating for the quiz.
        """
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(rating.rating for rating in ratings) / ratings.count()
        return 0.0
    
    def get_average_rating_html(self):
        """
        Get the average rating as HTML.
        """
        average_rating = self.get_average_rating()
        stars = int(average_rating)
        half_star = 1 if average_rating - stars >= 0.5 else 0
        empty_stars = 5 - stars - half_star
        return f"{'<i class="bi bi-star-fill"></i>' * stars}{'<i class="bi bi-star-half"></i>' * half_star}{'<i class="bi bi-star"></i>' * empty_stars}"

    def get_rating_for_user(self, user):
        """
        Get the rating given by a specific user for the quiz.
        """
        rating = self.ratings.filter(user=user).first()
        return rating.rating if rating else None
    
    def get_average_score(self):
        """
        Calculate the average score for the quiz.
        """
        attempts = self.attempts.all()
        if attempts.exists():
            score_value = sum(attempt.score for attempt in attempts) / attempts.count()
            average_score = (int(score_value / 10) / 10) * self.get_question_count()
            
            if average_score.is_integer():
                return int(average_score)
            return average_score

        return 0

    def get_is_saved_for_later(self, user):
        """
        Check if the quiz is saved for later by the user.
        """
        return self.saved_for_later.filter(user=user).exists()
    
    def get_questions(self):
        questions = Question.objects.filter(quiz=self)
        return questions
    
    def get_question_count(self):
        """
        Get the number of questions in the quiz.
        """
        return self.get_questions().count()
    
    def get_number_of_attempts(self):
        """
        Get the number of attempts for the quiz.
        """
        return self.attempts.count()
    
    def get_attempts_for_user(self, user):
        """
        Get the attempts for the quiz by a specific user.
        """
        return self.attempts.filter(user=user)
    
    def get_leaderboard(self, number_of_users=10):
        """
        Get the leaderboard for the quiz, showing only the highest score for each user.
        """
        all_attempts = self.attempts.all()
        best_attempts = {}
        
        for attempt in all_attempts:
            user_id = attempt.user_id
            if user_id not in best_attempts or attempt.score > best_attempts[user_id].score:
                best_attempts[user_id] = attempt
        
        sorted_attempts = sorted(best_attempts.values(), key=lambda x: x.score, reverse=True)
        return sorted_attempts[:number_of_users]


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
        return f"{self.user.username} - {self.quiz.name} - {self.score}"
    

class SavedForLater(models.Model):
    """
    SavedForLater model representing a quiz saved for later by a user.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='saved_for_later')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_for_later')

    def __str__(self):
        return f"{self.user.username} - {self.quiz.name}"
