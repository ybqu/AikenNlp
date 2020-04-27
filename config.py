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
from util import Util
from apps.metaphor.SimileExtraction.model.BertCRF import BertCRF


os.environ['CUDA_VISIBLE_DEVICES']='1'


ROOT_DIR = os.path.join(os.environ['HOME'], 'model')  # 模型目录

""" 1. 加载 Bert 模型 """

""" 1.1 加载 Bert 中文模型 """

BERT_ZH_MODEL_DIR = os.path.join(ROOT_DIR, 'bert-base-chinese')  # 模型目录
BERT_ZH_CONFIG = BertConfig.from_pretrained(BERT_ZH_MODEL_DIR + '/config.json')
BERT_ZH_TOKENIZER = BertTokenizer.from_pretrained(BERT_ZH_MODEL_DIR)
BERT_ZH_MODEL = BertForMaskedLM.from_pretrained(BERT_ZH_MODEL_DIR, config=BERT_ZH_CONFIG)

""" 1.2 加载 Bert 英文模型 """
BERT_EN_MODEL_DIR = os.path.join(ROOT_DIR, 'bert-base-uncased')  # 模型目录
BERT_EN_CONFIG = BertConfig.from_pretrained(BERT_EN_MODEL_DIR + '/config.json')
BERT_EN_TOKENIZER = BertTokenizer.from_pretrained(BERT_EN_MODEL_DIR)
BERT_EN_MODEL = BertForMaskedLM.from_pretrained(BERT_EN_MODEL_DIR, config=BERT_EN_CONFIG)

""" 2. 加载 GPT-2 模型 """
GPT2_TOKENIZER = tokenization_bert.BertTokenizer(vocab_file=ROOT_DIR + '/vocab_small.txt')

""" 2.1 加载 BaiduBaike 训练模型 """
GPT2_BK_MODEL = GPT2LMHeadModel.from_pretrained(ROOT_DIR + '/gpt2-baike-chinese')

""" 2.2 加载 LLKT 训练模型 """
GPT2_ES_MODEL = GPT2LMHeadModel.from_pretrained(ROOT_DIR + '/gpt2-essay-chinese')  # 加载模型

""" 3. 加载 simile extraction 模型 """

SIMILE_MODEL_DIR = os.path.join(ROOT_DIR, 'simile_labeling')

SIMILE_TOKENIZER = BertTokenizer.from_pretrained(SIMILE_MODEL_DIR)

num_labels, label_map = Util.metaphor_label()

SIMILE_MODEL = BertCRF.from_pretrained(SIMILE_MODEL_DIR, num_labels=num_labels, label_map=label_map)
