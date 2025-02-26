from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'weight', 'height', 'bio', 'profile_picture']

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



# class SurveyForm(forms.Form):
#     age = forms.IntegerField(label='Age', min_value=18)
#     weight = forms.FloatField(label='Weight (kg)')
#     height = forms.FloatField(label='Height (cm)')
#     fitness_goal = forms.ChoiceField(label='Fitness Goal', choices=[
#         ('lose_weight', 'Lose Weight'),
#         ('gain_muscle', 'Gain Muscle'),
#         ('maintain', 'Maintain Weight'),
#     ])
#     activity_level = forms.ChoiceField(label='Activity Level', choices=[
#         ('low', 'Low'),
#         ('moderate', 'Moderate'),
#         ('high', 'High'),
#     ])
#     food_preferences = forms.CharField(label='Food Preferences', max_length=100, required=False)




from django import forms
from .models import SurveyQuestion

class SurveyForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField()
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    weight = forms.FloatField()
    height = forms.FloatField()
    health_conditions = forms.CharField(widget=forms.Textarea, required=False)
    preference = forms.ChoiceField(choices=[('Vegetarian', 'Vegetarian'), ('Non-Vegetarian', 'Non-Vegetarian')])
    goal = forms.ChoiceField(choices=[('Weight Loss', 'Weight Loss'), ('Muscle Gain', 'Muscle Gain'), ('Maintenance', 'Maintenance')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for question in SurveyQuestion.objects.all():
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=[(option, option) for option in question.options],
                label=question.question_text
            )

