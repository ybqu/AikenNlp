#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   urls.py
@Time    :   2020/04/21 12:55:49
@Author  :   Aiken 
@Version :   1.0
@Contact :   2191002033@cnu.edu.cn
@License :   
@Desc    :   None
'''

# here put the import lib
from django.urls import path
from . import views

urlpatterns = [
    path('website/', views.website),
    path('author/', views.author),
]
