
# 用户

from django.db import models
# Django提供的一个AbstractUser类，可以自由定制我们需要的model
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
class UserProfile(AbstractUser):
    gender_choices = (
        ('male','男'),
        ('female','女'),
    )
    nick_name = models.CharField('昵称',max_length=50, default='')
    birthday = models.DateField('生日', null=True,blank=True)
    gender = models.CharField('性别', max_length=10, choices=gender_choices,default='female')
    adress = models.CharField('地址',max_length=  100, default='')
    mobile = models.CharField('手机号',max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to = 'image/%Y%m',default='image/default.png', max_length=100)

    class Meta:
        # 指明一个易于理解和表述的对象名称，单数形式
        # 如果这个值没有设置，Django将使用该model的类名的分词形式作为他的对象表述名
        verbose_name = '用户信息'
        # 对象的复数表述名
        verbose_name_plural = verbose_name
        db_table = 'UserProfile'

    def __str__(self):
        return self.username


# 验证码
class EmailVerifyRecord(models.Model):
    send_choices = (
        ('register','注册'),
        ('forget','找回密码'),
    )
    code = models.CharField('验证码',max_length=20)
    email = models.EmailField('邮箱',max_length=15)
    send_type = models.CharField(choices=send_choices,max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
        db_table = 'EmailVerifyRecode'


# 轮播图
class Banner(models.Model):
    title = models.CharField('标题',max_length=100)
    image = models.ImageField('轮播图',upload_to='banner/%Y%m',max_length=100)
    url = models.URLField('访问地址',max_length=100)
    index = models.IntegerField('顺序',default=100)
    add_time = models.DateTimeField('添加时间',default=datetime.now)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
        db_table = 'Banner'
