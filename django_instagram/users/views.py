from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .forms import SignUpForm

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
     

def signup(request):
    if request.method == "GET":
        form =SignUpForm()

        return render(request, 'users/signup.html', {'form': form})
    
    elif request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
             user=form.save(commit=False)
             user.set_password(form.cleaned_data['password1'])
             user.save()

             #로그인 처리 시작
             username =form.cleaned_data['username']
             password = form.cleaned_data['password1']
             user = authenticate(request, username=username, password=password)

             if user is not None:
                 login(request, user)
                 #로그인 처리 끝
                 return HttpResponseRedirect(reverse('posts:index'))
                 # 폼 유효성 검사 실패 시        

        # 폼 유효성 검사 실패 시
        else:
          return render(request, 'users/signup.html', {'form': form})
        
    # 실패시 오류 메시지 전달
    return render(request, 'users/main.html', {'error_message': '회원가입에 실패 하였습니다.'})













           
    


    

