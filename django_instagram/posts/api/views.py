from django.shortcuts import get_object_or_404
from django_instagram.users.models import User as user_model
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django_instagram.posts.models import Post
from .serializers import PostSerializer , CommentFormSerializer
from django.db.models import Q
from django_instagram.posts.forms import CommentForm
from django_instagram.posts import models 
from django.http import JsonResponse

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def get_queryset(self):
        """현재 사용자의 게시글과 팔로잉한 사용자의 게시글을 가져옴"""
        user = get_object_or_404(user_model, pk=self.request.user.id)
        following = user.following.all()
        return Post.objects.filter(Q(author__in=following) | Q(author=user)).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        loginUser = request.user  # 현재 로그인한 사용자 객체
        serializer = self.get_serializer(queryset, many=True, context={'request': request})        
        #ListAPIView는 DRF 기반이므로 Response를 사용
        return Response({"posts": serializer.data, "loginUser": loginUser.username}, status=status.HTTP_200_OK)



def posts_list_view(request):
    if request.method == 'GET':
        user = get_object_or_404(user_model, pk=request.user.id)
        following = user.following.all() 
        loginUser = request.user  # 현재 로그인한 사용자 객체
        # 게시글 필터링  __ 언더바 포함의미 caption__contains ==>캡션 포함이 되어 있는 것        
        followed_posts = models.Post.objects.filter(Q(author__in=following) | Q(author=user)).order_by('-created_at')

        # 시리얼라이저로 데이터 변환
        serializer = PostSerializer(followed_posts, many=True, context={'request': request})
        return JsonResponse({"posts": serializer.data,"loginUser": loginUser.username},  status=200)




class PostDetailView(generics.RetrieveAPIView):
      pass