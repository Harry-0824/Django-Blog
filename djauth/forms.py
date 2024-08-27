from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required':'請輸入使用者名稱',
        'max_length':'長度在2~20之間',
        'min_length':'長度在2~20之間'
    })
    password = forms.CharField(max_length=20,min_length=6,error_messages={
        'required':'請輸入密碼',
        'max_length':'長度在8~20之間',
        'min_length':'長度在8~20之間'
    })
    email = forms.EmailField(error_messages={
        'required':'請輸入信箱',
        'invalid':'信箱格式不正確'
    })
    captcha = forms.CharField(max_length=4, min_length=4)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('信箱已被註冊!')
        return email
    
    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')
        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError('驗證碼不符!')
        captcha_model.delete()
        return captcha

class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={
        'required':'請輸入信箱',
        'invalid':'信箱格式不正確'
    })
    password = forms.CharField(max_length=20,min_length=6,error_messages={
        'required':'請輸入密碼',
        'max_length':'長度在8~20之間',
        'min_length':'長度在8~20之間'
    })
    remember = forms.IntegerField(required=False)