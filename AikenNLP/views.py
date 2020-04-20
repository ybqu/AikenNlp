#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   views.py
@Time    :   2020/04/21 00:22:15
@Author  :   Aiken 
@Version :   1.0
@Contact :   2191002033@cnu.edu.cn
@License :   
@Desc    :   None
'''

# here put the import lib
from django.shortcuts import render, HttpResponse

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')