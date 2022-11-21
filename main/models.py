from datetime import datetime
from django.db import models
from taggit.managers import TaggableManager

class Post(models.Model):
    date = models.DateTimeField(default=datetime.now(), blank=True)
    title = models.CharField(max_length=350, verbose_name='Название поста', unique=True, blank=True)
    anons = models.CharField(max_length=500, verbose_name='Анонс поста', blank=True)
    text = models.TextField(verbose_name='Текст поста', blank=True)
    tags = TaggableManager(blank=False, verbose_name='Тэг поста')
    image = models.ImageField(upload_to='post_images\img', verbose_name='Изображение поста', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        pass


class Comment(models.Model):
    date = models.DateTimeField(default=datetime.now(), blank=True)
    author = models.CharField(max_length=45, verbose_name='Имя комментатора')
    comment = models.CharField(max_length=255, verbose_name='Комментарий')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default="", verbose_name='Пост')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        pass
