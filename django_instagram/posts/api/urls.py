from django.urls import path
from .views import PostListView ,PostLikeView
from . import views


app_name = "posts_api"  # 네임스페이스 충돌 방지

urlpatterns = [
    
    # 게시글 목록
    # get : http://localhost:8000/api/posts/
    path("posts/", PostListView.as_view(), name="posts-list"),  # /api/posts/

    # get : http://localhost:8000/api/posts/list
    path("posts/list", views.posts_list_view , name="posts-list"),  # /api/posts/list


    # 좋아요 추가 및 취소 
    # post :  http://localhost:8000/api/1/post_like
    path('posts/<int:post_id>/post_like/', PostLikeView.as_view(), name='post_like'),


]