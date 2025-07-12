from django.urls import path
from . import views

app_name="users"
urlpatterns = [
    path('', views.main, name="main"),
    path('signup/', views.signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
]
