#! /usr/bin/env python
# -*- coding: utf-8 -*-

import xadmin
from .models import *

class CourseAdmin(object):
    # 显示的列
    list_display = ['name','desc','detail','degree','learn_times','students']
    # 搜索
    search_fields = ['name','desc','detail','degree','student']
    # 过滤
    list_filter = ['name','desc','detail','degree','learn_times','students']

class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    # 这里的course__name是根据课程名称来过滤的
    list_filter =  ['course__name','name','add_time']

class VedioAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson', 'name', 'add_time']

class CourseResourceAdmin(object):
    list_display = ['course','name', 'download','add_time']
    search_fields = ['course','name', 'download']
    list_filter = ['course__name','name', 'download','add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Vedio,VedioAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)