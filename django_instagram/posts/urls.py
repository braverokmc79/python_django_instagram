from django.urls import path
from . import views
from django.urls import include

app_name = "posts"

urlpatterns = [
     path('', views.index, name="index"),

     # 게시글 생성
     # /posts/create/
     path('create/', views.post_create, name='post_create'),

     # 게시글 삭제   :  /posts/1/post_delete
     path('<int:post_id>/post_delete/', views.post_delete, name='post_delete'),



     #댓글 생성
     # /posts/1/comment_create/
     path('<int:post_id>/comment_create/', views.comment_create, name='comment_create'),

     #댓글 삭제
     # /posts/1/comment_delete/
     path('<int:comment_id>/comment_delete/', views.comment_delete, name='comment_delete'),

]