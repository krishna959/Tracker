from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserForm, UserProfileForm, UserRegisterForm
from .models import UserProfile
from .forms import SurveyForm

@login_required
def profile_view(request):
    """
    View for displaying and updating the user profile.
    """
    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=request.user.userprofile)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')

    return render(request, 'users/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
    })


def custom_login_view(request):
    """
    Custom login view to authenticate users.
    Redirects to the survey page after successful login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to survey page after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'users/login.html')


def register(request):
    """
    View for user registration.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please log in.')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    """
    Log out the user and redirect to the login page.
    """
    logout(request)
    return redirect('login')



from django.shortcuts import render
from .models import DietPlan
@login_required
def survey(request):
    if request.method == "POST":
        age = int(request.POST.get("age"))
        height = int(request.POST.get("height"))
        weight = int(request.POST.get("weight"))
        goal = request.POST.get("goal")
        activity_level = request.POST.get("activity_level", "moderate")

        # store data in session
        request.session["age"] = age
        request.session["height"] = height
        request.session["weight"] = weight
        request.session["goal"] = goal
        request.session["activity_level"] = activity_level

        # ✅ Calculate BMR (Basal Metabolic Rate)
        bmr = 10 * weight + 6.25 * height - 5 * age + 5  # For males (use -161 for females)

        # ✅ Adjust BMR based on activity level
        activity_multipliers = {
            "low": 1.2,
            "moderate": 1.55,
            "high": 1.9
        }
        tdee = bmr * activity_multipliers.get(activity_level, 1.55)  # Default to "moderate"

        # ✅ Modify calories based on goal
        if goal == "muscle_gain":
            calories = tdee + 300  # Add 300 kcal for muscle gain
        elif goal == "weight_loss":
            calories = tdee - 500  # Subtract 500 kcal for weight loss
        else:
            calories = tdee  # Maintenance calories

        # ✅ Find the best diet plan based on user input
        diet_plan = DietPlan.objects.filter(
            min_age__lte=age, max_age__gt=age,  # Fix for age selection
            min_height__lte=height, max_height__gte=height,
            min_weight__lte=weight, max_weight__gte=weight,
            goal=goal,
           
        ).first()

        return render(request, "users/diet_plan.html", {
            "diet_plan": diet_plan,
            "age": age,
            "height": height,
            "weight": weight,
            "goal": goal,
            "activity_level": activity_level,
            "calories": round(calories)  # Send the **exact calorie calculation**
        })

    return render(request, "users/survey.html")
