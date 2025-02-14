from django.shortcuts import render , get_object_or_404 ,redirect
from django_instagram.users.models import User as user_model  # 사용자 모델 import
from . import models 
from .forms import CreatePostForm
from django.db.models import Q
from .api import serializers
from django.http import JsonResponse , HttpResponse
from django.urls import reverse

# Create your views here.
def index2(request):
    if request.method == 'GET': 
        if request.user.is_authenticated:
            """
                models.Post.objects.filter(...):

                1.models.Post: Post는 게시글 모델로, 데이터베이스의 게시글 테이블과 매핑된 Django 모델입니다.
                    1).objects: 모델에 대해 데이터베이스 쿼리를 실행할 수 있는 관리 매니저입니다.
                    2).filter(): 특정 조건에 해당하는 레코드만 필터링하여 반환하는 ORM 메서드입니다.
                
                2.Q 객체:
                    **Q**는 Django의 ORM에서 OR 조건을 처리하거나 복잡한 조건을 생성할 때 사용하는 객체입니다.
                    
            
                3.결과:
                    posts 변수에는 다음 두 조건을 만족하는 게시글들이 저장됩니다
                    1)팔로우 중인 사용자가 작성한 게시글
                    2)현재 사용자가 작성한 게시글


                4.author__in :author__in은 변수로 저장되는 것이 아니라 author__in은 쿼리를 생성하기 위한 조건 설정에만 사용됩니다.
                    1)author 필드:
                        Post 모델의 author 필드입니다. 이 필드는 ForeignKey로 연결되어 있으며, 게시글의 작성자를 나타냅니다
                    2)_in 룩업:
                        Django의 쿼리 필터링 옵션 중 하나로, 특정 값들의 리스트, 쿼리셋, 또는 iterable 객체 안에 포함된 레코드를 조회합니다.
                        예) models.Post.objects.filter(author__in=[user1, user2]) 여기서 author가 user1 또는 user2인 게시글을 필터링합니다.
            """           
            # 사용자 정보 가져오기
            user = get_object_or_404(user_model, pk=request.user.id)
            following=user.following.all()
            posts=models.Post.objects.filter(
                    Q(author__in=following) | Q(author=user)
            )

            serializer = serializers.PostSerializer(posts, many=True, context={'request': request})
            print(serializer.data)
            #return JsonResponse(serializer.data, safe=False)
            return render(request, 'posts/index.html', {"posts": serializer.data})

    return  redirect(reverse('users:main') ) #인증 되지 않는 사용자 로그인화면으로



def index(request):
    if request.method == 'GET': 
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)                        
            return render(request, 'posts/index.html', {"user": user})
    return  redirect(reverse('users:main') ) 




def post_create(request):
    if request.method == "GET":
        form = CreatePostForm()
        return render(request, 'posts/post_create.html', {'form': form})

    elif request.method == "POST":
        # 사용자 인증 여부 확인
        if request.user.is_authenticated:
          # 요청한 사용자 정보 가져오기
           user =get_object_or_404(user_model, pk=request.user.id)

           # 이미지와 캡션 값 가져오기
           # image = request.FILES.get("image")  # 이미지 파일이 없을 경우 None 반환
           # caption = request.POST.get("caption")  # 캡션이 없을 경우 None 반환

           # # 게시글 생성
           # new_post = models.Post.objects.create(
           #     author=user,  # 작성자 설정
           #     image=image,  # 이미지 설정
           #     caption=caption  # 캡션 설정
           # )
           # new_post.save()  # 저장

           form=CreatePostForm(request.POST, request.FILES)
           if form.is_valid():
              new_post = form.save(commit=False)
              new_post.author = user
              new_post.save()
              return redirect(reverse('posts:index'))
           else:
              return render(request, 'posts/post_create.html', {'form': form})
           
        else:
             # 인증되지 않은 사용자는 에러 메시지와 함께 로그인 페이지로 이동
            return render(request, 'users/main.html', {'error_message': '권한오류: post 등록에 실패하였습니다.'})