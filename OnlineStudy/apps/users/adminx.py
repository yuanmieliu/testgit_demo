#! /usr/bin/env python
# -*- coding: utf-8 -*-

import xadmin
from xadmin import views
from .models import EmailVerifyRecord,Banner

# xadmin这里继承的是object，不再是继承admin
class EmailVerifyRecordAdmin(object):
    # 显示的列
    list_display = ['code','email','send_type','send_time']
    # 搜索的字段，不添加时间搜索
    search_fields = ['code','email','send_type']
    # 过滤
    list_filter = ['code','email','send_type','send_time']

class BannerAdmin(object):
    # 显示的列
    list_display = ['title','image','url','index','add_time']
    # 搜索的字段
    search_fields = ['title','image','url','index']
    # 过滤
    list_filter = ['title', 'image', 'url', 'index', 'add_time']

# 创建xadmin的最基本管理器配置，并与view绑定
class BaseSettings(object):
    # 开启注意功能
    enable_themes = True
    use_bootswatch = True

# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = '火星人在线学习系统'
    # 修改footer
    site_footer = '我学习，我快乐'
    # 收起菜单
    menu_style = 'accordion'

xadmin.site.register(views.CommAdminView,GlobalSettings)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSettings)


