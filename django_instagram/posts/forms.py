from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption", "image"]

        labels = {
            "caption": "내용",
            "image": "사진"
        }

    def clean_caption(self):
        caption = self.cleaned_data.get("caption")
        if len(caption) < 10:  #  내용이 10자 이상이어야 한다는 유효성 검사
            raise forms.ValidationError("내용은 최소 10자 이상이어야 합니다.")
        return caption

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:  # 이미지가 존재하는 경우에만 검사
            if not image.name.endswith(('.png', '.jpg', '.jpeg')):  # 이미지 확장자 체크
                raise forms.ValidationError("지원하는 이미지 형식은 PNG, JPG, JPEG입니다.")
        return image
