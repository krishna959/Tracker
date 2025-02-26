from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    duration = models.DurationField()  # e.g., 00:30:00
    calories_burned = models.FloatField()
    date = models.DateField(auto_now_add=True)

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=100)
    calories_consumed = models.FloatField()
    date = models.DateField(auto_now_add=True)

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_weight = models.FloatField()
    weekly_exercise_hours = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

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

