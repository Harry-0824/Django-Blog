from django import forms
from .models import BlogCategory, Profile  # 假设你有一个BlogCategory模型

class PubBlogForm(forms.Form):
    title = forms.CharField(
        max_length=100, 
        min_length=2,
        error_messages={
            'required': '请填写标题',
            'min_length': '标题长度不能少于2个字符',
            'max_length': '标题长度不能超过100个字符',
        }
    )
    content = forms.CharField(
        min_length=2, 
        widget=forms.Textarea,
        error_messages={
            'required': '请填写内容',
            'min_length': '内容长度不能少于2个字符',
        }
    )
    category = forms.IntegerField()


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']