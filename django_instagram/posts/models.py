from django.db import models
from django_instagram.users import models as user_models
from django.utils.translation import gettext_lazy as _


# 공통 등록일과 수정일
class TimeStampedModel(models.Model):
     created_at = models.DateTimeField(_("생성일"), auto_now_add=True)
     updated_at = models.DateTimeField(_("수정일"), auto_now=True)

     class Meta:
          abstract = True


#게시글
class Post(TimeStampedModel):
    author = models.ForeignKey(
        user_models.User, 
        null=True, #여기서 null 은 데이터 베이스에 관련된 null 허용 여부
        on_delete=models.CASCADE, 
        related_name='post_author', 
        verbose_name=_("작성자")
    )
    image = models.ImageField(_("이미지"), upload_to="posts/", blank=False)
    caption = models.TextField(_("내용"), blank=False)#여기서 blank 유효성 검사를 위한 허용여부
    image_likes = models.ManyToManyField(
        user_models.User, 
        blank=True,  
        related_name='post_image_likes',         
        verbose_name=_("좋아요")
    )

    """
    1)가독성 향상:
    관리 화면(admin)에서 모델 객체가 기본적으로 Post object (1) 또는 Comment object (1)처럼 보일 수 있는데,
      __str__을 정의하면 더 읽기 쉬운 형태로 나타납니다.   
    2)디버깅 편의성 : 객체를 디버깅하거나 로깅할 때, 객체의 의미 있는 정보를 바로 확인할 수 있습니다. 
    """
    def __str__(self):
        return f"{self.author} : {self.caption}"

    class Meta:
        verbose_name = _("게시물")
        verbose_name_plural = _("게시물들")
        ordering = ['-created_at']  # 최신 게시물이 먼저 오도록 기본 정렬


#댓글
class Comment(TimeStampedModel):
    author = models.ForeignKey(
        user_models.User, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='comment_author',   
        verbose_name=_("작성자")
    )
    post = models.ForeignKey(
        Post, 
        null=True, 
        on_delete=models.CASCADE, 
        related_name='comment_post',
        verbose_name=_("게시물")
    )
    contents = models.TextField(_("내용"), blank=True)

    def __str__(self):
        return f"{self.author} : {self.contents[:20]}"  # 댓글 미리보기 (20자까지)
    
    class Meta:
        verbose_name = _("댓글")
        verbose_name_plural = _("댓글들")
        ordering = ['-created_at']  # 최신 댓글이 먼저 오도록 설정