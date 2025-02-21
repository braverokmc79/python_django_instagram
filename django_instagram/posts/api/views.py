from django.shortcuts import get_object_or_404
from django_instagram.users.models import User as user_model
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django_instagram.posts.models import Post
from .serializers import PostSerializer , CommentFormSerializer ,UserSerializer
from django.db.models import Q, Count
from django_instagram.posts.forms import CommentForm
from django_instagram.posts import models 
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator




# 1.전체 게시글을 가져오되,  
class PostAllListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """현재 사용자의 게시글을 먼저 가져오고, 나머지 최신 게시글을 포함하여 정렬"""
        user = get_object_or_404(user_model, pk=self.request.user.id)
        search_keyword = self.request.GET.get('q', "")

        # 1️⃣ 현재 사용자의 게시글을 먼저 가져옴
        user_posts = Post.objects.filter(author=user, caption__icontains=search_keyword)

        # 2️⃣ 현재 사용자의 게시글을 제외한 전체 최신 게시글을 가져옴
        other_posts = Post.objects.filter(Q(caption__icontains=search_keyword)).exclude(author=user)

        # 3️⃣ 현재 사용자의 게시글을 먼저 배치하고, 최신순으로 정렬
        #현재 사용자의 게시글을 우선적으로 정렬
        #(user_posts | other_posts)

        #현재 사용자 글 제외한 글
        queryset = ( other_posts).order_by(
            # 현재 사용자의 게시글을 먼저 정렬하고 최신순으로 정렬
            '-author_id',  # 현재 사용자의 글을 우선적으로 배치 (임시 정렬)
            '-created_at'  # 최신 글 순서대로 정렬
        )
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # 4️⃣ 페이징 처리
        page = self.request.GET.get('page', 1)
        page_size = self.request.GET.get('pageSize', 5)
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)

        # 5️⃣ 직렬화 (JSON 변환)
        serializer = self.get_serializer(page_obj, many=True, context={'request': request})
        login_user_serializer = UserSerializer(request.user, context={'request': request})

        # 6️⃣ 응답 반환
        return Response({
            "posts": serializer.data,  # 게시글 목록
            "loginUser": login_user_serializer.data,  # 현재 로그인한 사용자 정보
            "has_next": page_obj.has_next(),  # 다음 페이지 여부
            "total_pages": paginator.num_pages  # 총 페이지 수
        }, status=status.HTTP_200_OK)



#2.현재 사용자의 게시글 팔로잉 게시글
# http://localhost:8000/posts/
#1)  목록 : Django REST Framework(DRF)의 generics.ListAPIView 는class PostListView(generics.ListAPIView):
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """현재 사용자의 게시글을 우선적으로 가져오고, 좋아요가 많고 최신 게시물을 포함하여 정렬"""
        user = get_object_or_404(user_model, pk=self.request.user.id)
        search_keyword = self.request.GET.get('q', "")
        following = user.following.all()

        # 현재 사용자의 게시글과 팔로잉 유저의 게시글을 DB에서 필터링
        queryset = Post.objects.filter(Q(author=user) | Q(author__in=following),caption__icontains=search_keyword
        ).annotate(like_count=Count('image_likes')).order_by('-author', '-like_count', '-created_at')

        return queryset

    def list(self, request, *args, **kwargs):    
        queryset = self.get_queryset()

        # ✅ 여기서 DB에 실제로 쿼리가 실행됨 (LIMIT 적용)
        page = self.request.GET.get('page', 1)
        page_size = self.request.GET.get('pageSize', 5)
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page) # ✅ 여기서 DB에서 데이터를 가져옴


        # 시리얼라이저로 데이터 변환- ❌ get_serializer() 자체는 쿼리를 실행하지 않음
        serializer = self.get_serializer(page_obj, many=True, context={'request': request})
        #로그인한 유저 정보 가져오기
        login_user_serializer = UserSerializer(request.user, context={'request': request})

        return Response({
            "posts": serializer.data,
            "loginUser": login_user_serializer.data,
            "has_next": page_obj.has_next(),
            "total_pages": paginator.num_pages
        }, status=status.HTTP_200_OK)







#2) 목록 : Django의 일반 함수형 뷰(FBV, Function-Based View) 
@api_view(['GET'])
def posts_list_view(request):
    if request.method == 'GET':
        user = get_object_or_404(user_model, pk=request.user.id)
        following = user.following.all()       
        # 게시글 필터링  __ 언더바 포함의미 caption__contains ==>캡션 포함이 되어 있는 것        
        followed_posts = models.Post.objects.filter(Q(author__in=following) | Q(author=user)).order_by('-created_at')

        # 시리얼라이저로 데이터 변환
        serializer = PostSerializer(followed_posts, many=True, context={'request': request})

         # 현재 로그인한 사용자 정보를 UserSerializer로 변환
        login_user_serializer = UserSerializer(request.user, context={'request': request}) 
        return JsonResponse({"posts": serializer.data,"loginUser": login_user_serializer.data},  status=200)




# FBV : 검색 목록 처리
def posts_search_list(request):
    """
    AJAX 요청을 처리하여 특정 페이지의 게시글을 반환합니다.
    """
    if request.method == 'GET':
        page = request.GET.get('page', 1)  # 요청된 페이지 번호
        user = request.user
        following = user.following.all() if user.is_authenticated else []
        
        searchKeyword = request.GET.get('q', "")
        pageSize = request.GET.get('pageSize', 5) # 페이지당 2개

        # 게시글 필터링  __ 언더바 포함의미 caption__contains ==>캡션 포함이 되어 있는 것
        followed_posts = models.Post.objects.filter(
           ( Q(author__in=following) | Q(author=user) ) & Q(caption__contains=searchKeyword)
        ) if user.is_authenticated else models.Post.objects.none()

        other_posts = models.Post.objects.exclude(author__in=following).exclude(author=user).filter(caption__contains=searchKeyword)

        # 모든 게시글 합치기
        posts = (followed_posts | other_posts).order_by('-created_at')

        # 페이징 처리
        paginator = Paginator(posts, pageSize)  
        page_obj = paginator.get_page(page)

        # 시리얼라이저로 데이터 변환
        serializer = PostSerializer(page_obj, many=True, context={'request': request})

        return JsonResponse({
            "posts": serializer.data,
            "has_next": page_obj.has_next(),  # 다음 페이지 여부
        })



# 
# FBV : 일반 함수 장고 뷰방식 :좋아요 추가 및 취소
@require_POST
@login_required
def post_like(request, post_id):
    post = get_object_or_404(models.Post, pk=post_id)

    try:

        # ManyToManyField 에 한에서 기본적으로 중복 관계를 허용하지 않으므로, filter(pk=...)와 
        # .exists()만으로 충분히 유니크한 관계를 확인할 수 있습니다. 
        if post.image_likes.filter(pk=request.user.pk).exists():
            post.image_likes.remove(request.user)
            is_added = False
        else:
            post.image_likes.add(request.user)
            is_added = True

        return JsonResponse({"success": True,"message": "like" if is_added else "dislike",
                            "like_count": post.image_likes.count(),}, status=200)

    except Exception as e:
        return JsonResponse({"success": False, "message": "오류가 발생했습니다.", "error": str(e)}, status=500)
    


# DRF  : 좋아요 추가 및 취소
class PostLikeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        """좋아요 추가 및 취소 기능"""
        post = get_object_or_404(models.Post, pk=post_id)
        user =request.user

        if post.image_likes.filter(pk=user.pk).exists():
            post.image_likes.remove(user)
            is_added = False
        else:
            post.image_likes.add(user)
            is_added = True

        return Response({"success": True,"message": "like" if is_added else "dislike",
                        "like_count": post.image_likes.count(),}, status=status.HTTP_200_OK)



