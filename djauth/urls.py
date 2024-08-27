from django.urls import path
from . import views
app_name = 'djauth'

urlpatterns = [
    path('login', views.djlogin, name='login'),
    path('register', views.register, name='register'),
    path('captcha', views.send_email_captcha, name='captcha'),
    path('logout', views.djlogout, name='logout')
]