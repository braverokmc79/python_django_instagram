from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


def main(request):
    if request.method == "GET":
        return render(request, 'users/main.html')

    elif request.method == "POST":
        # POST 데이터 가져오기
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"POST 방식 파라미터 가져오기: {username}, {password}")

        # 사용자 인증
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 로그인 처리
            login(request, user)
            return HttpResponseRedirect(reverse('posts:index'))
        else:
            # 실패 시 오류 메시지 전달
            return render(request, 'users/main.html', {'error_message': '아이디 또는 비밀번호가 맞지 않습니다.'})
        

       
    


    

