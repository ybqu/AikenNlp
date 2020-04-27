#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   config.py
@Time    :   2020/04/21 17:10:46
@Author  :   Aiken 
@Version :   1.0
@Contact :   2191002033@cnu.edu.cn
@License :   
@Desc    :   None
'''

# here put the import lib
import os
from apps.writeai.tokenizations import tokenization_bert
from transformers import BertConfig
from transformers import BertTokenizer, BertModel, BertForMaskedLM
from transformers import GPT2LMHeadModel

os.environ['CUDA_VISIBLE_DEVICES']='1'


""" 1. 加载 Bert 模型 """

BERT_MODEL_DIR = os.path.join(os.environ['HOME'], 'sources/bert')  # 模型目录

""" 1.1 加载 Bert 中文模型 """

BERT_ZH_CONFIG = BertConfig.from_pretrained(BERT_MODEL_DIR + '/bert-base-chinese/config.json')
BERT_ZH_TOKENIZER = BertTokenizer.from_pretrained(BERT_MODEL_DIR + '/bert-base-chinese')
BERT_ZH_MODEL = BertForMaskedLM.from_pretrained(BERT_MODEL_DIR + '/bert-base-chinese', config=BERT_ZH_CONFIG)

""" 1.2 加载 Bert 英文模型 """
BERT_EN_CONFIG = BertConfig.from_pretrained(BERT_MODEL_DIR + '/bert-base-uncased/config.json')
BERT_EN_TOKENIZER = BertTokenizer.from_pretrained(BERT_MODEL_DIR + '/bert-base-uncased')
BERT_EN_MODEL = BertForMaskedLM.from_pretrained(BERT_MODEL_DIR + '/bert-base-uncased', config=BERT_EN_CONFIG)

""" 2. 加载 GPT-2 模型 """
GPT2_MODEL_DIR = os.path.join(os.environ['HOME'], 'sources/gpt2')  # 模型目录
GPT2_TOKENIZER = tokenization_bert.BertTokenizer(vocab_file=GPT2_MODEL_DIR + '/vocab_small.txt')

""" 2.1 加载 BaiduBaike 训练模型 """
GPT2_BK_MODEL = GPT2LMHeadModel.from_pretrained(GPT2_MODEL_DIR + '/gpt2-baike-chinese')

""" 2.2 加载 LLKT 训练模型 """
GPT2_ES_MODEL = GPT2LMHeadModel.from_pretrained(GPT2_MODEL_DIR + '/gpt2-essay-chinese')  # 加载模型

