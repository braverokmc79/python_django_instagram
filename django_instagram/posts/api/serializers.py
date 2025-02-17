from rest_framework import serializers
from django_instagram.users.models import User as user_model
from .. import models
from django.middleware.csrf import get_token

#유저 모델
class FeedAuthorSerializer(serializers.ModelSerializer):    
    class Meta:
        model = user_model
        fields = (
            "id",
            "username",
            "profile_photo",
        )


class CommentSerializer(serializers.ModelSerializer):
    # author의 username을 매핑하여 username 하나만 가져올경우
    #username  = serializers.CharField(source='author.username')  
    
    #유저에 관련된 정보 가져오기
    author = FeedAuthorSerializer()

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'contents',
            "author",
            #"username",
        )




class PostSerializer(serializers.ModelSerializer):
    #댓글 가져오기
    comment_post = CommentSerializer(many=True)  # related_name='comment_post' 필요    
    #유저정보 가져오기
    author = FeedAuthorSerializer()
    #보안을 위해  csrf 토큰 가져옴
    csrf_token =serializers.SerializerMethodField()  

    class Meta:
        model = models.Post
        fields = (
            "id",
            "image",
            "caption",
            "image_likes",
            "author",
            "comment_post",
            "csrf_token",            
        )
        
    def get_csrf_token(self, obj):
        # 요청 객체에서 CSRF 토큰 가져오기
        request = self.context.get('request')
        return get_token(request) if request else None
    


class CommentFormSerializer(serializers.Serializer):
    fields = serializers.SerializerMethodField()

    def get_fields(self, obj):
        return {field_name: str(field.field.widget.attrs) for field_name, field in obj.fields.items()}




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = (
            "id",
            "username",
            "email",
            "profile_photo",
            "bio",
        )
