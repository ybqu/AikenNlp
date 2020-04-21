#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   models.py
@Time    :   2020/04/21 18:08:21
@Author  :   Aiken 
@Version :   1.0
@Contact :   2191002033@cnu.edu.cn
@License :   
@Desc    :   None
'''

# here put the import lib
import random
import torch
import config
import torch.nn.functional as F
from django.db import models

# Create your models here.
class Bert_Masked(models.Model):

    @staticmethod
    def get_prediction(lan, sentence):
        # 加载模型
        if lan == 'ZH':
            tokenizer = config.BERT_ZH_TOKENIZER
            model = config.BERT_ZH_MODEL
        elif lan == 'EN':
            tokenizer = config.BERT_EN_TOKENIZER
            model = config.BERT_EN_MODEL

        input_ids = torch.tensor(tokenizer.encode(sentence)).unsqueeze(0)

        index_list = []

        for i, id in enumerate(input_ids[0]):
            if id == 103:
                index_list.append(i)

        # 切换到 gpu 上运行
        if torch.cuda.is_available():
            input_ids = input_ids.to('cuda')
            model.to('cuda')

        outputs = model(input_ids, masked_lm_labels=input_ids)
        loss, prediction_scores = outputs[:2]

        # 对预测后的分数做 softmax 取前5个最大值
        sm_result = F.softmax(prediction_scores, dim=2)
        topk_values, topk_indices = sm_result.topk(5, dim=2)[:2]

        # 取出预测词 values 和 indices
        mask_values = (topk_values[0][index_list]).tolist()
        mask_indices = (topk_indices[0][index_list]).tolist()

        # 将预测词 decode
        for i, indices in enumerate(mask_indices):
            # mask_indices[i] = tokenizer.decode(indices).split(' ')
            for j, indice in enumerate(indices):
                mask_indices[i][j] = tokenizer.decode(indice).replace(' ', '')
                
        return {'values': mask_values, 'indices': mask_indices}, len(index_list)
