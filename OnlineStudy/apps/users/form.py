#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField

# 登录表单验证
class LoginForm(forms.Form):
    # 用户名和密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


# 注册验证表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # 验证码，字段里面可以自定义错误提示信息
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})


# 忘记密码表单验证
class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})

# 重置密码表单
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
