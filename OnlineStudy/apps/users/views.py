from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import UserProfile,EmailVerifyRecord
from django.views.generic.base import View
from .form import *
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email

# Create your views here.

# 邮箱和用户名可以登录
# 基础ModuleBackend,因为他有authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个get失败的一个原因是Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username)|Q(email = username))
            # djangod的后台中密码加密：所以不能password == password
            # UserProfile继承的AbstractUser中有def check_password(self,raw+password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None



class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        # 实例化
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 获取用户提交的用户名和密码
            user_name = request.POST.get('username',None)
            pass_word = request.POST.get('password',None)
            # 成功返回user对象，失败None
            user = authenticate(username = user_name,password = pass_word)
            # 如果不是null说明验证成功
            if user is not None:
                if user.is_active:
                    # 只有注册激活才能登录
                    login(request,user)
                    return render(request,'index.html')
                # 只有当用户名或密码不存在时，才返回错误信息到前端
                else:
                    return render(request,'login.html',{'msg':'用户名或密码错误','login_form':login_form})
            # 只有当用户名和密码不存在时，才返回错误信息到前端
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误','login_form':login_form})
        # form.is_valid()已经判断不合法了，所以这里不需要再返回错误信息到前端了
        else:
            return render(request,'login.html',{'msg':'用户名或密码错误','login_form':login_form})

# 激活用户
class ActivateUserView(View):
    def get(self,request,activate_code):
        # 查询邮箱验证记录是否存在
        all_recode = EmailVerifyRecord.objects.filter(code=activate_code)

        if all_recode:
            for recode in all_recode:
                # 获取到对应的邮箱
                email = recode.email
                # 查询到邮箱对应的user
                user = UserProfile.objects.get(email = email)
                user.is_active = True
                user.save()
        #验证码不对的时候，跳转到激活失败页面
        else:
            return render(request,'active_fail.html')
        # 激活成功跳转到登录页面
        return render(request, 'login.html')

class RegisterView(View):
    '''用户注册'''
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('emaile', None)
            # 如果用户已存在，则提示错误信息
            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':'用户已存在'})
            pass_word = request.POST.get('password',None)
            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对保存到数据库的密码加密
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request,'register.html',{'register_form':register_form})


'''
如果是get请求，直接返回注册页面给用户
如果是post请求，先生成一个表单实例，并获取用户提交的所有信息（request.POST）
is_valid()方法，验证用户的提交信息是不是合法
如果合法，获取用户提交的email和password
实例化一个user_profile对象，把用户添加到数据库
默认添加的用户是激活状态（is_active=1表示True），在这里我们修改默认的状态（改为is_active = False），只有用户去邮箱激活之后才改为True
对密码加密，然后保存，发送邮箱，user
注册成功跳转到登录界面
'''

class ForgetPwdView(View):
    # 找回密码
    def get(self,request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('eamil',None)
            send_register_email(email,'forget')
            return render(request, 'send_success.html')
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})

class ResetView(View):
    def get(self,request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for recode in all_records:
                email = recode.email
                return render(request, 'password_reset.html',{'eamil':email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')

class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'密码不一致！'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, 'login.html')
        else:
            email = request.POST.get('email','')
            return render(request, 'password_reset.html', {'email':email, 'modify_form':modify_form})


