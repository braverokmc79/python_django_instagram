from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    GENDER_CHOICES = (
        ('M', _('남성')),
        ('F', _('여성')),
        ('C', _('사용자 지정')),
    )

    # Django의 기본 first_name, last_name 필드를 제거
    #first_name = None  
    #last_name = None  

    name = models.CharField(_("사용자 이름"), blank=True, max_length=255)
    user_name = models.CharField(_("아이디"), blank=True, max_length=255)  
    profile_photo = models.ImageField(_("프로필 사진"), blank=True, upload_to="profile_pics/") #파일 경로 지정
    website = models.URLField(_("웹사이트"), blank=True, max_length=255)
    bio = models.TextField(_("소개"), blank=True)
    email = models.EmailField(_("이메일"), blank=False)
    phone_number = models.CharField(_("전화번호"), blank=True, max_length=20)  
    gender = models.CharField(_("성별"), blank=True, choices=GENDER_CHOICES, max_length=5)

    # ✅ ManyToManyField에 blank=True 추가
    #A가 B를 팔로우한다고 해서, B가 A를 자동으로 팔로우하는 것은 아닙니다. 이런 경우 symmetrical=False를 설정해야 합니다.
    followers = models.ManyToManyField(
        "self", verbose_name=_("팔로워"), symmetrical=False, related_name="user_followers", blank=True
    )
    following = models.ManyToManyField(
        "self", verbose_name=_("팔로잉"), symmetrical=False, related_name="user_following", blank=True
    )

    def get_absolute_url(self) -> str:
        """사용자의 상세 페이지 URL 반환"""
        return reverse("users:detail", kwargs={"username": self.username})
