#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   getData.py
@Time    :   2020/04/27 15:35:11
@Author  :   Aiken 
@Version :   1.0
@Contact :   2191002033@cnu.edu.cn
@License :   
@Desc    :   None
'''

# here put the import lib
# from .MetaphorModel import Config
import os
import random
filepath = os.path.dirname(os.path.abspath(__file__))


def get_sentences():
    """
    ? 获取句子
    """
    sentence_label = []
    sentences = []
    labels = []

    with open(filepath + '/data/test.txt', 'r+', encoding='utf8') as f:
        lines = f.readlines()
        
        sentence = []
        label = []
        for line in lines:
            line = line.strip().split()
            if len(line) == 1:
                sentence_label.append(int(line[0]))
            elif len(line) == 0:
                sentences.append(''.join(sentence))
                labels.append(' '.join(label))
                sentence = []
                label = []
            else:
                sentence.append(line[0])
                label.append(line[1])
    return sentence_label, sentences, labels