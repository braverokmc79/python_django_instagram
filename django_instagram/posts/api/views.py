from django.shortcuts import get_object_or_404
from django_instagram.users.models import User as user_model
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django_instagram.posts.models import Post
from .serializers import PostSerializer
from django.db.models import Q

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def get_queryset(self):
        """현재 사용자의 게시글과 팔로잉한 사용자의 게시글을 가져옴"""
        user = get_object_or_404(user_model, pk=self.request.user.id)
        following = user.following.all()
        return Post.objects.filter(Q(author__in=following) | Q(author=user))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDetailView(generics.RetrieveAPIView):
      pass