from django.urls import path
from .views import PostListView ,PostDetailView
from . import views
app_name = "posts_api"  # 네임스페이스 충돌 방지

urlpatterns = [
    path("posts/", PostListView.as_view(), name="posts-list"),  # /api/posts/
    path("posts/list", views.posts_list_view , name="posts-list"),  # /api/posts/list

    
    path("posts/<int:pk>/", PostDetailView.as_view(), name="posts-detail"),  # /api/posts/<id>/
]