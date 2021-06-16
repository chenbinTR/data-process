#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author ChenOT
@desc 
@date 2021/6/16
"""

from django.urls import path   #导入路径相关配置
from django.conf.urls import include, url
from . import  views  #导入视图views

urlpatterns = [
    path('', views.scan_pen_sevice),  #默认访问book业务的首页
    # url(r'^ocr/v1$', views.scan_pen_sevice)
]