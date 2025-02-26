from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('', custom_login_view, name='login'),
    # path('custom-login/', custom_login_view, name='login'),  # Add this line
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('survey/', survey, name='survey'),
]
