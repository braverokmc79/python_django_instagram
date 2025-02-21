from django.urls import path
from .views import PostAllListView ,PostListView ,PostLikeView
from . import views


app_name = "posts_api"  # 네임스페이스 충돌 방지

#1.현재 사용자의 게시글과 전체 최신 게시글
#2.현재 사용자의 게시글 팔로잉 게시글
urlpatterns = [
    
    # 1.현재 사용자의 게시글과 전체 최신 게시글
    # get : http://localhost:8000/api/posts/
    path("all/posts/", PostAllListView.as_view(), name="api_posts"),  # /api/posts/

    # 2.현재 사용자의 게시글 팔로잉 게시글
    # get : http://localhost:8000/api/posts/
    path("posts/", PostListView.as_view(), name="api_posts"),  # /api/posts/


    # get : http://localhost:8000/api/posts/list
    path("posts/list", views.posts_list_view , name="api_posts_list"),  # /api/posts/list


    # /api/posts/searchList
    path('posts/searchList/', views.posts_search_list, name='api_posts_searchList'),


    # 좋아요 추가 및 취소 
    # post :  http://localhost:8000/api/1/post_like
    path('posts/<int:post_id>/post_like/', PostLikeView.as_view(), name='post_like'),

]