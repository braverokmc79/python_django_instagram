from django.shortcuts import render , get_object_or_404
from django_instagram.users.models import User as user_model  # 사용자 모델 import
from . import models  , serializers

# Create your views here.
def index(request):
    return render(request, 'posts/index.html')

def post_create(request):
    if request.method == "GET":
        return render(request, 'posts/post_create.html')

    elif request.method == "POST":
        if request.user.is_authenticated:

           user =get_object_or_404(user_model, pk=request.user.id)

           image =request.FILES['image']
           caption=request.POST['caption']

           new_post=models.Post.objects.create(
                author=user,
                image=image,
                caption=caption,
           )
           new_post.save()

           return render(request, 'posts/base.html')
        
        else:
           return render(request, 'posts/post_create.html')