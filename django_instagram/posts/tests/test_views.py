from django.core.files.uploadedfile import SimpleUploadedFile  # 테스트용 파일 업로드 클래스
from django.contrib.auth import get_user_model  # 유저 모델을 가져오는 유틸리티 함수
from django.urls import reverse  # URL 리버스 함수
from django.test import TestCase  # Django의 테스트 케이스 클래스


class TestPosts(TestCase):
    """
    게시글(Post) 관련 기능에 대한 테스트 케이스.
    - 게시글 작성 페이지 접근
    - 게시글 생성
    - 로그인 여부에 따른 동작 테스트
    """

    def setUp(self):
        """
        테스트 실행 전 초기 설정.
        테스트용 유저를 생성하여 로그인 및 인증 테스트에 사용합니다.
        """
        User = get_user_model()  # 현재 프로젝트의 User 모델 가져오기
        self.user = User.objects.create_user(
            username='testuser',  # 사용자 이름
            email='testuser@example.com',  # 이메일 주소
            password='testpassword'  # 비밀번호
        )

    def test_get_posts_page(self):
        """
        게시글 작성 페이지로 GET 요청을 테스트합니다.
        - 요청 성공 여부 확인 (HTTP 200)
        - 올바른 템플릿이 사용되었는지 확인
        """
        url = reverse('posts:post_create')  # 게시글 작성 페이지의 URL 가져오기
        response = self.client.get(url)  # GET 요청 실행

        # HTTP 상태 코드가 200인지 확인
        self.assertEqual(response.status_code, 200)

        # 올바른 템플릿이 사용되었는지 확인
        self.assertTemplateUsed(response, 'posts/post_create.html')

 