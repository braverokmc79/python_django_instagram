from django.urls import path
from .views import PostListView ,PostDetailView

app_name = "posts_api"  # 네임스페이스 충돌 방지

urlpatterns = [
    path("posts/", PostListView.as_view(), name="posts-list"),  # /api/posts/
    path("posts/<int:pk>/", PostDetailView.as_view(), name="posts-detail"),  # /api/posts/<id>/
]