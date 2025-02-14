from django.urls import path
from . import views
from django.urls import include

app_name = "posts"

urlpatterns = [
     path('', views.index, name="index"),
     path('create/', views.post_create, name='post_create'),
]