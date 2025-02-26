from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import DietPlan
from .forms import ActivityForm, MealForm
from .models import Activity, Meal
# from tracker import models
from django.db.models import Sum


@login_required
def dashboard(request):
    user = request.user  # Ensure user is authenticated

    # ✅ Get session data
    age = request.session.get("age", 25)
    height = request.session.get("height", 170)
    weight = request.session.get("weight", 70)
    goal = request.session.get("goal", "general")
    activity_level = request.session.get("activity_level", "moderate")

    # ✅ Calculate BMR
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
    activity_multipliers = {"low": 1.2, "moderate": 1.55, "high": 1.9}
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)

    # ✅ Modify calories based on goal
    if goal == "muscle_gain":
        calories = tdee + 300
    elif goal == "weight_loss":
        calories = tdee - 500
    else:
        calories = tdee  # Maintenance

    # ✅ Fetch Diet Plan
    diet_plan = DietPlan.objects.filter(
        min_age__lte=age, max_age__gt=age,
        min_height__lte=height, max_height__gte=height,
        min_weight__lte=weight, max_weight__gte=weight,
        goal=goal,
    ).first()

    # ✅ Fetch User Activities
    activities = Activity.objects.filter(user=user).order_by('-id')
    meals = Meal.objects.filter(user=user).order_by('-id')

    # ✅ Calculate total calories burned
    total_calories_burned = Activity.objects.filter(user=request.user).aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0

    # calculate total calorie intake
    total_calories_consumed = Meal.objects.filter(user=request.user).aggregate(Sum('calories_consumed'))['calories_consumed__sum'] or 0

    remaining_calories = round(calories - total_calories_burned+total_calories_consumed)
    total_calorie = round(total_calories_burned-total_calories_consumed)


    # ✅ Debugging Logs
    print(f"Calories Passed to Template: {calories}")
    print(f"Total Calories Burned: {total_calories_burned}")

    return render(request, "tracker/dashboard.html", {
        "diet_plan": diet_plan,
        "calories": round(calories),
        "age": age,
        "height": height,
        "weight": weight,
        "goal": goal,
        "activities": activities,
        "meals": meals,
        "total_calories_burned": total_calories_burned , # Passing total burned calories
        "total_calories_consumed": total_calories_consumed,
        "remaining_calories": remaining_calories,
        "total_calorie": total_calorie,
    })



@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            
            # ✅ Calculate total calories burned
            total_calories_burned = Activity.objects.filter(user=request.user).aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0

            
            # ✅ Store in session (optional)
            request.session['total_calories_burned'] = total_calories_burned
            
            return redirect('dashboard')
    else:
        form = ActivityForm()
    
    return render(request, 'tracker/add_activity.html', {'form': form})



@login_required
def add_meal(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()

            total_calories_consumed = Meal.objects.filter(user=request.user).aggregate(Sum('calories_consumed'))['calories_consumed__sum'] or 0

            # store in session
            request.session['total_calories_consumed'] = total_calories_consumed

            return redirect('dashboard')
    else:
        form = MealForm()
    return render(request, 'tracker/add_meal.html', {'form': form})


@login_required
def delete_activity(request, activity_id):
    activity = get_object_or_404(Activity, id=activity_id, user=request.user)
    if request.method == "POST":
        activity.delete()
    return redirect("dashboard")  # Redirect back to the dashboard

@login_required
def delete_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    if request.method == "POST":
        meal.delete()
    return redirect("dashboard")  # Redirect back to the dashboard

from django.shortcuts import render

# def dashboard(request):
#     dark_mode = request.COOKIES.get('dark_mode', 'light')  # Default to 'light' mode
#     return render(request, 'tracker/dashboard.html', {'dark_mode': dark_mode})


