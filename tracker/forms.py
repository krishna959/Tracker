from django import forms
from .models import Activity, Meal, Goal

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['activity_type', 'duration', 'calories_burned']

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['meal_name', 'calories_consumed']

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['target_weight', 'weekly_exercise_hours', 'start_date', 'end_date']
