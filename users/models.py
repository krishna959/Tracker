from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)  # in kilograms
    height = models.FloatField(null=True, blank=True)  # in centimeters
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def bmi(self):
        """Calculate the BMI (Body Mass Index)."""
        if self.height and self.weight:
            height_in_meters = self.height / 100
            return round(self.weight / (height_in_meters ** 2), 2)
        return None





from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    weight = models.FloatField()
    height = models.FloatField()
    health_conditions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SurveyQuestion(models.Model):
    question_text = models.TextField()
    options = models.JSONField()

    def __str__(self):
        return self.question_text

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    response = models.TextField()

    def __str__(self):
        return f"{self.user.name} - {self.question.question_text}"



from django.db import models

class DietPlan(models.Model):
    min_age = models.IntegerField(default=18)
    max_age = models.IntegerField(default=30)
    min_height = models.IntegerField(default=160)
    max_height = models.IntegerField(default=180)
    min_weight = models.IntegerField(default=50)
    max_weight = models.IntegerField(default=80)
    goal = models.CharField(max_length=20, default="general")
    diet_plan = models.TextField(default="")
    image_urls = models.TextField(default="")
    

    def get_image_list(self):
        """Convert comma-separated image URLs into a list."""
        return self.image_urls.split(",")

    def __str__(self):
        return f"{self.goal} - {self.min_age}-{self.max_age} years - {self.diet_plan} - {self.image_urls}"

