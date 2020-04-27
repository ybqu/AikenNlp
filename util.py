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

    @staticmethod
    def get_metaphor_labels():
        """ 
        ? 获取隐喻 label
        """
        return ['PAD', 'CLS', 'SEP', "START", "STOP", "O", "ss", "sb", "si", "se", "ts", "tb", "ti", "te", "aps", "apb", "api", "ape", "vps", "vpb", "vpe", "vpi"]

    @staticmethod
    def metaphor_label():
        """ 
        ? 获取隐喻 label 相关数据
        """
        label_list = Util.get_metaphor_labels()

        label_map = {label: i for i, label in enumerate(label_list)}
        num_labels = len(label_list)
        return num_labels, label_map
