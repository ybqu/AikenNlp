#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   util.py
@Time    :   2020/04/23 10:48:32
@Author  :   Aiken 
@Version :   1.0
@Contact :   2191002033@cnu.edu.cn
@License :   
@Desc    :   工具类
'''

# here put the import lib
class Util():
    @staticmethod
    def returnData(code, msg, count, data):
        """
        ? 定义后端返回数据格式 
        """
        return {"code": code,  "msg": msg, "count": count,"data": data}