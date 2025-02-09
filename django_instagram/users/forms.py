from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.utils.translation import gettext_lazy as _
from django import forms as django_forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """



# 회원 가입폼 추가
#강의와 다르게 django_forms.ModelForm 이 아니라 password1, password2 사용을 위해, UserCreationForm을 상속받아서 사용
class SignUpForm(UserCreationForm):  
    class Meta:
        model = User

        classStyle = """w-full p-3 border border-gray-300 rounded-lg text-sm 
                        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"""

        fileInputStyle=""" file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold 
                        file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer """

        # UserCreationForm의 비밀번호 필드를 포함시키고, 추가적인 필드를 포함
        fields = ("email", "name", "username", "profile_photo", "website", "bio", "gender", "password1", "password2")
        
        # 위젯 설정
        widgets = {
            'email': django_forms.EmailInput(attrs={'placeholder':'이메일',  'required': 'required', 'class': classStyle}),
            'name': django_forms.TextInput(attrs={'placeholder':'성명', 'required': 'required', 'class': classStyle}),
            'username': django_forms.TextInput(attrs={'placeholder':'사용자이름(아이디)', 'required': 'required', 'class': classStyle}),
            'profile_photo': django_forms.ClearableFileInput(attrs={'placeholder':'프로필 사진', 'class': classStyle + fileInputStyle }),
            'website': django_forms.URLInput(attrs={'placeholder':'웹사이트', 'class': classStyle}),
            'bio': django_forms.Textarea(attrs={'placeholder':'소개', 'class': classStyle +" h-32"}),
            'gender': django_forms.Select(attrs={'placeholder':'성별',  'class': classStyle, 'required': 'required'}),           
        }
        
        labels = {
            'email': '이메일',
            'name': '성명',
            'username': '사용자이름(아이디)',
            'profile_photo': '프로필 사진',
            'website': '웹사이트',
            'bio': '소개',
            'gender': '성별',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # password1, password2 위젯 스타일 적용
        self.fields['password1'].widget.attrs.update({'placeholder':'비밀번호','class': self.Meta.classStyle, 'required': 'required'})
        self.fields['password2'].widget.attrs.update({'placeholder':'비밀번호 확인', 'class': self.Meta.classStyle, 'required': 'required'})

    # 추가적으로 커스터마이징할 수 있는 방법: 
    # 비밀번호 확인 로직을 커스터마이징하고 싶으면, `clean` 메서드를 오버라이드 할 수 있습니다.
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")      

        # 비밀번호 확인이 일치하지 않으면 에러를 발생시킬 수 있습니다.
        if password1 != password2:
            raise django_forms.ValidationError("비밀번호가 일치하지 않습니다.")

        return cleaned_data



    
