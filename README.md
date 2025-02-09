# django_instagram

To-do:
--------
- [] 포스트 생성
- [] 포스트 수정
- [] 포스트 삭제
- [] 포스트 리스트(피드)
- [] 댓글
- [] 좋아요
- [] 검색
- [] 프로필 피드

--------



파이썬 장고(Python Django) - 쿠키커터(Cookiecutter)로 만드는 Instagram + TailwindCSS 프로젝트

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

라이선스: macaroncs.net


## 설정

설정 관련 내용은 [settings 문서](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html)에서 확인하세요.

## 기본 명령어

### 사용자 설정

- **일반 사용자 계정**을 생성하려면, 회원가입(Sign Up) 페이지에서 양식을 작성하세요. 제출 후 "이메일 주소를 확인하세요" 페이지가 나타납니다. 콘솔에서 이메일 인증 메시지를 확인한 후 제공된 링크를 브라우저에 입력하면 이메일 인증이 완료됩니다.

- **관리자(superuser) 계정**을 생성하려면, 다음 명령어를 실행하세요:

      $ python manage.py createsuperuser

  
일반 사용자는 Chrome에서, 관리자 계정은 Firefox에서 로그인하면 두 계정의 동작을 비교할 수 있습니다.

### 타입 검사

mypy를 사용하여 타입 검사를 실행하려면:

    $ mypy django_instagram

### 테스트 커버리지

테스트를 실행하고 커버리지를 확인하며, HTML 보고서를 생성하려면 다음 명령어를 사용하세요:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### pytest를 사용한 테스트 실행

    $ pytest

### 라이브 리로딩 및 SASS CSS 컴파일

관련 내용은 [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp) 문서를 참고하세요.

## 배포

이 애플리케이션을 배포하는 방법은 아래와 같습니다.

