from django import forms
from .models import Post, Comment

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
        if len(caption) < 5:  # 내용이 5자 이상이어야 한다는 유효성 검사
            raise forms.ValidationError("내용은 최소 5자 이상이어야 합니다.")
        return caption

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image is None:
            raise forms.ValidationError("이미지를 업로드해야 합니다.")  # 필수 입력 필드라면 추가

        if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise forms.ValidationError("지원하는 이미지 형식은 PNG, JPG, JPEG입니다.")
        
        return image



class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption", "image"]

        labels = {
            "caption": "내용",
            "image": "사진"
        }

    def clean_caption(self):
        caption = self.cleaned_data.get("caption")
        if len(caption) < 5:  #  내용이 5자 이상이어야 한다는 유효성 검사
            raise forms.ValidationError("내용은 최소 5자 이상이어야 합니다.")
        return caption

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:  # 이미지가 존재하는 경우에만 검사
            if not image.name.endswith(('.png', '.jpg', '.jpeg')):  # 이미지 확장자 체크
                raise forms.ValidationError("지원하는 이미지 형식은 PNG, JPG, JPEG입니다.")
        return image




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contents']
        labels = {
            "contents": "",
        }
        widgets = {
            "contents": forms.Textarea(attrs={
                "placeholder": "댓글을 입력하세요...",
                "rows": 3,
            }),
        }

    def clean_contents(self):
        contents = self.cleaned_data.get("contents", "").strip()
        
        if not contents:  # 빈 문자열 또는 공백만 입력한 경우
            raise forms.ValidationError("댓글 내용을 입력해주세요.")

        if len(contents) < 2:  # 최소 2자 이상 입력
            raise forms.ValidationError("댓글은 최소 2자 이상 입력해야 합니다.")

        if len(contents) > 100:  # 최대 100자 제한
            raise forms.ValidationError("댓글은 100자 이하로 입력해야 합니다.")

        return contents


