from django.shortcuts import render , get_object_or_404
from django_instagram.users.models import User as user_model  # 사용자 모델 import
from . import models 
from .forms import CreatePostForm

# Create your views here.
def index(request):
    return render(request, 'posts/index.html')

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
              return render(request, 'posts/main.html')
           else:
              return render(request, 'posts/post_create.html', {'form': form})
           
        else:
             # 인증되지 않은 사용자는 에러 메시지와 함께 로그인 페이지로 이동
            return render(request, 'users/main.html', {'error_message': '권한오류: post 등록에 실패하였습니다.'})