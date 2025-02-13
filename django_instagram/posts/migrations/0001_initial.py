# Generated by Django 5.0.11 on 2025-02-13 03:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('image', models.ImageField(upload_to='posts/', verbose_name='이미지')),
                ('caption', models.TextField(verbose_name='내용')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_author', to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
                ('image_likes', models.ManyToManyField(blank=True, related_name='post_image_likes', to=settings.AUTH_USER_MODEL, verbose_name='좋아요')),
            ],
            options={
                'verbose_name': '게시물',
                'verbose_name_plural': '게시물들',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('contents', models.TextField(blank=True, verbose_name='내용')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_author', to=settings.AUTH_USER_MODEL, verbose_name='작성자')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_post', to='posts.post', verbose_name='게시물')),
            ],
            options={
                'verbose_name': '댓글',
                'verbose_name_plural': '댓글들',
                'ordering': ['-created_at'],
            },
        ),
    ]
