from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class BlogCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='分類名稱')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '文章分類'
        verbose_name_plural = verbose_name

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='標題')
    content = models.TextField(verbose_name='內容')
    pub_time = models.DateTimeField(auto_now=True, verbose_name='發布時間')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, verbose_name='分類')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    def __str__(self):
       return self.title

    class Meta:
        verbose_name = '部落格'
        verbose_name_plural = verbose_name
        ordering = ['-pub_time']

class BlogComment(models.Model):
    content = models.TextField(verbose_name='內容')
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name='發布時間')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,related_name='comments', verbose_name='所屬部落格')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    def __str__(self):
       return self.content

    class Meta:
        verbose_name = '評論'
        verbose_name_plural = verbose_name
        ordering = ['-pub_time']

AVATAR_CHOICES = [
    ('avatar1.png', '吉依卡哇'),
    ('avatar2.png', '小八貓'),
    ('avatar3.png', '小八貓2'),
    ('avatar4.png', '烏薩奇')
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=100, choices=AVATAR_CHOICES, default='avatar1.png')
    
    def __str__(self):
       return self.user.username