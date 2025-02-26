from django.urls import path

from tracker import views



urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-activity/', views.add_activity, name='add_activity'),
    path('add-meal/', views.add_meal, name='add_meal'),
    path("delete-activity/<int:activity_id>/", views.delete_activity, name="delete_activity"),
    path("delete-meal/<int:meal_id>/", views.delete_meal, name="delete_meal"),
    # path('',)
]

