# django\_instagram

> 코담 편저

파이썬 장고(Python Django) - 쿠키커터(Cookiecutter)로 만드는 **Instagram + TailwindCSS** 프로젝트

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


---

## 📌 To-do

* 포스트 생성
* ] 포스트 수정
*  포스트 삭제
* 포스트 리스트(피드)
* 댓글 기능
* 좋아요 기능
* 검색 기능
*  프로필 피드


## 편저: [코담](https://codam.kr/)

### 파이썬·장고 웹개발 | 코담 - 코드에 세상을 담다

[![코담 소개 이미지](https://codam.kr/assets/images/og-image.jpg)](https://codam.kr/)

---



## ⚙️ 설정

설정 관련 자세한 정보는 [Cookiecutter Django Settings 문서](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html)를 참고하세요.

---

## 💠 기본 명령어

### 👤 사용자 설정

* **일반 사용자 계정 생성**
  회원가입(Sign Up) 페이지에서 양식을 작성합니다.
  제주 후 "이메일 주소를 확인하세요" 안내가 나오며,
  콘솔에 표시된 이메일 인증 링크를 브라우저에 입력하면 인증이 완료됩니다.

* **관리자(superuser) 계정 생성**
  콘솔에서 다음 명령어 실행:

  ```bash
  python manage.py createsuperuser
  ```

Chrome에서는 일반 사용자로, Firefox에서는 관리자 계정으로 로그인하여 동작을 비교해보시면 됩니다.

---

### ✅ 타입 검사

```bash
mypy django_instagram
```

---

### 🧪 테스트 & 커버리지 확인

```bash
coverage run -m pytest
coverage html
open htmlcov/index.html
```

### 또는 단순히 테스트만 실행하려면:

```bash
pytest
```

---

### ♻️ 라이브 리로딩 및 SASS 커피밌

TailwindCSS 및 SASS 관련 설정은 아래 문서를 참고하세요:
🔗 [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp)

---

## 🚀 배포

배포 관련 내용은 Cookiecutter Django 공식 문서에서 단계별 가이드를 확인하세요.

---

> 본 프로젝트는 컴파일 과정을 위해 사용하는 역할을 해요. 교육 및 클론 코딩 목적으로 제작되어있습니다.
