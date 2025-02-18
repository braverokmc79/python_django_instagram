from django.shortcuts import render , get_object_or_404 ,redirect
from django_instagram.users.models import User as user_model  # 사용자 모델 import
from . import models 
from .forms import CreatePostForm,UpdatePostForm, CommentForm
from django.db.models import Q
from .api import serializers
from django.http import JsonResponse , HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django_instagram.utils import form_errors_to_string  # 공통 함수 가져오기

# def index2(request):
#     if request.method == 'GET': 
#         if request.user.is_authenticated:
#             """
#                 models.Post.objects.filter(...):

#                 1.models.Post: Post는 게시글 모델로, 데이터베이스의 게시글 테이블과 매핑된 Django 모델입니다.
#                     1).objects: 모델에 대해 데이터베이스 쿼리를 실행할 수 있는 관리 매니저입니다.
#                     2).filter(): 특정 조건에 해당하는 레코드만 필터링하여 반환하는 ORM 메서드입니다.
                
#                 2.Q 객체:
#                     **Q**는 Django의 ORM에서 OR 조건을 처리하거나 복잡한 조건을 생성할 때 사용하는 객체입니다.
                    
            
#                 3.결과:
#                     posts 변수에는 다음 두 조건을 만족하는 게시글들이 저장됩니다
#                     1)팔로우 중인 사용자가 작성한 게시글
#                     2)현재 사용자가 작성한 게시글


#                 4.author__in :author__in은 변수로 저장되는 것이 아니라 author__in은 쿼리를 생성하기 위한 조건 설정에만 사용됩니다.
#                     1)author 필드:
#                         Post 모델의 author 필드입니다. 이 필드는 ForeignKey로 연결되어 있으며, 게시글의 작성자를 나타냅니다
#                     2)_in 룩업:
#                         Django의 쿼리 필터링 옵션 중 하나로, 특정 값들의 리스트, 쿼리셋, 또는 iterable 객체 안에 포함된 레코드를 조회합니다.
#                         예) models.Post.objects.filter(author__in=[user1, user2]) 여기서 author가 user1 또는 user2인 게시글을 필터링합니다.
#             """           
#             # 사용자 정보 가져오기
#             user = get_object_or_404(user_model, pk=request.user.id)
#             following=user.following.all()
#             posts=models.Post.objects.filter(
#                     Q(author__in=following) | Q(author=user)
#             )

#             serializer = serializers.PostSerializer(posts, many=True, context={'request': request})
#             print(serializer.data)
#             #return JsonResponse(serializer.data, safe=False)
#             return render(request, 'posts/index.html', {"posts": serializer.data})

#     return  redirect(reverse('users:main') ) #인증 되지 않는 사용자 로그인화면으로


def index(request):
    if request.method == 'GET': 
        if request.user.is_authenticated:
            user = get_object_or_404(user_model, pk=request.user.id)                
            return render(request, 'posts/index.html', {"user": user})
    return  redirect(reverse('users:main') ) 



# 게시글 생성
@login_required
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
              # 유효성 검사 실패 시 오류 메시지 전달
              return render(request, 'posts/post_create.html', {'form': form})
           



# 게시글 삭제
@require_http_methods(["DELETE"])
@login_required
def post_delete(request, post_id):
    post=get_object_or_404(models.Post, pk=post_id )
    
    if post.author == request.user:
        post.delete()
        return JsonResponse({"success": True, "message": "게시글 삭제되었습니다."}, status=200)
    
    return JsonResponse({"success": False, "message": "삭제 권한이 없습니다."}, status=403)



#게시글 수정
@login_required
def post_update(request, post_id):
    post = get_object_or_404(models.Post, pk=post_id)    
    if post.author!= request.user:
        return redirect(reverse('users:main'))
    
    if request.method == "GET":
        form = UpdatePostForm(instance=post)
        return render(request, 'posts/post_update.html', {'form': form, 'post': post})
    
    elif request.method == "POST":
        #instance=post → 기존 객체를 폼에 채우고 수정 가능하도록 함.
        form = UpdatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
           # 이미지 파일이 없는 경우 원래 이미지 유지
            if not request.FILES.get('image'):
                form.instance.image = post.image  # 기존 이미지 유지

             # 변경 사항 저장
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('posts:index'))
        else:
            # 유효성 검사 실패 시 오류 메시지 전달
            return render(request, 'posts/post_update.html', {'form': form, 'post': post})
            




# 댓글 생성
@require_POST
def comment_create(request, post_id):
    # 인증 확인 먼저 수행
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "로그인이 필요합니다."}, status=401)

    # 게시글 존재 여부 확인
    post = get_object_or_404(models.Post, pk=post_id)

    # 댓글 폼 처리
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return JsonResponse({"success": True, "comment": serializers.CommentSerializer(comment).data})
    
    # 수정: 유효성 검사 실패 시 오류 메시지를 "error" 키에 담아 반환
    # error_list = []
    # for msgs in form.errors.values():  # 각 필드의 에러 메시지 리스트를 가져옴
    #     for msg in msgs:  # 그 리스트 내부의 개별 메시지를 가져옴
    #         error_list.append(msg)
    #============한줄로 변경처리리==========>
    # error_messages = " ".join([msg for msgs in form.errors.values() for msg in msgs])  
    #print("dderror_messages", error_messages)

    # 유효성 검사 실패 시 오류 메시지 반환
    return JsonResponse({
        "success": False,
        "message": "댓글 등록 실패",
        "errors": form_errors_to_string(form)   # 폼 오류 메시지 포함
    }, status=400)



#댓글 삭제
@require_http_methods(["DELETE"])
@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(models.Comment, pk=comment_id)    

    if comment.author == request.user:
        comment.delete()
        return JsonResponse({"success": True, "message": "댓글이 삭제되었습니다."}, status=200)
    
    return JsonResponse({"success": False, "message": "삭제 권한이 없습니다."}, status=403)



