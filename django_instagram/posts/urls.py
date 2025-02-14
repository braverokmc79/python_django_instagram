from django.urls import path
from . import views
from django.urls import include

app_name = "posts"

urlpatterns = [
     path('', views.index, name="index"),
     path('create/', views.post_create, name='post_create'),


     #댓글 생성
     # /posts/1/comment_create/
     path('<int:post_id>/comment_create/', views.comment_create, name='comment_create'),

]