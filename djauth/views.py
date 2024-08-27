from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.http import HttpResponse
import string, random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout

User = get_user_model()

# Create your views here.
@require_http_methods(['GET', 'POST'])
def djlogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                #登入
                login(request, user)
                user.is_authenticated
                #是否需要記住我
                if not remember:
                    #如果未點擊記住我,網頁關閉後就過期
                    request.session.set_expiry(0)
                    #若有點擊,便使用默認的過期時間
                return redirect('/')
            else:
                print('信箱或密碼錯誤')
                form.add_error('email', '信箱或密碼錯誤')
                #return render(request, 'login.html', context={'form': form})
                return redirect(reverse('djauth:login'))

def djlogout(request):
    logout(request)
    return redirect('/')

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('djauth:login'))
        else:
            print(form.errors)
            #重新跳轉至註冊頁面
            return render(request, 'register.html', context={'form': form})
        

def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'errmsg': '请输入邮箱'})
    captcha = ''.join(random.sample(string.digits, 4))
    #儲存到資料庫
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail('註冊驗證碼', message=f'你的註冊驗證碼是{captcha}', recipient_list=[email], from_email=None)
    return JsonResponse({'code': 200, 'message': '發送成功'})