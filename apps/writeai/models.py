#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   models.py
@Time    :   2020/04/21 21:24:49
@Author  :   Aiken 
@Version :   1.0
@Contact :   2191002033@cnu.edu.cn
@License :   
@Desc    :   None
'''

# here put the import lib
import torch
import config
import torch.nn.functional as F
from django.db import models

# Create your models here.
class Writeai(models.Model):
    @staticmethod
    def _is_word(word):
        for item in list(word):
            if item not in 'qwertyuiopasdfghjklzxcvbnm':
                return False
        return True

    @staticmethod
    def _top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float('Inf')):
        # batch size 1 for now - could be updated for more but the code would be less clear
        assert logits.dim() == 1
        top_k = min(top_k, logits.size(-1))  # Safety check
        if top_k > 0:
            # Remove all tokens with a probability less than the last token of the top-k
            indices_to_remove = logits < torch.topk(logits, top_k)[
                0][..., -1, None]
            logits[indices_to_remove] = filter_value

        if top_p > 0.0:
            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
            cumulative_probs = torch.cumsum(
                F.softmax(sorted_logits, dim=-1), dim=-1)

            # Remove tokens with cumulative probability above the threshold
            sorted_indices_to_remove = cumulative_probs > top_p
            # Shift the indices to the right to keep also the first token above the threshold
            sorted_indices_to_remove[...,
                                     1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = 0

            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            logits[indices_to_remove] = filter_value
        return logits

    @staticmethod
    def _sample_sequence(model, context, length, position, n_ctx, tokenizer, temperature=1.0, top_k=30, top_p=0.0, repitition_penalty=1.0,
                         device='cpu'):
        context = torch.tensor(context, dtype=torch.long, device=device)
        context = context.unsqueeze(0)
        generated = context
        with torch.no_grad():
            for _ in range(length):
                inputs = {'input_ids': generated[0]
                          [-(n_ctx - 1):].unsqueeze(0)}
                outputs = model(
                    **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
                next_token_logits = outputs[0][0, -1, :]
                for id in set(generated):
                    next_token_logits[id] /= repitition_penalty
                next_token_logits = next_token_logits / temperature
                next_token_logits[tokenizer.convert_tokens_to_ids(
                    '[UNK]')] = -float('Inf')
                filtered_logits = Writeai._top_k_top_p_filtering(
                    next_token_logits, top_k=top_k, top_p=top_p)
                next_token = torch.multinomial(
                    F.softmax(filtered_logits, dim=-1), num_samples=1)
                generated = torch.cat((generated, next_token.unsqueeze(0)), dim=1)
        generated = generated[:, position:]
        return generated.tolist()[0]

    @staticmethod
    def generate(prefix, corpus='BK', length=-1, nsamples=5, batch_size=1, temperature=1, top_k=8, top_p=0, repetition_penalty=1.0):

        device = "cuda" if torch.cuda.is_available() else "cpu"

        tokenizer = config.GPT2_TOKENIZER
        
        if corpus == 'BK':
            model = config.GPT2_BK_MODEL
        elif corpus == 'LLKT':
            model = config.GPT2_ES_MODEL
            
        model.to(device)
        model.eval()

        n_ctx = model.config.n_ctx

        if length == -1:
            length = model.config.n_ctx

        data = []

        while True:
            raw_text = prefix
            position = len(prefix)
            context_tokens = tokenizer.convert_tokens_to_ids(
                tokenizer.tokenize(raw_text))
            generated = 0
            for _ in range(nsamples // batch_size):
                out = Writeai._sample_sequence(model, context_tokens, length, position, n_ctx, tokenizer=tokenizer, temperature=temperature, top_k=top_k, top_p=top_p,
                                               repitition_penalty=repetition_penalty, device=device)
                for i in range(batch_size):
                    generated += 1
                    text = tokenizer.convert_ids_to_tokens(out)
                    for i, item in enumerate(text[:-1]):  # 确保英文前后有空格
                        if Writeai._is_word(item) and Writeai._is_word(text[i + 1]):
                            text[i] = item + ' '
                    for i, item in enumerate(text):
                        if item == '[MASK]':
                            text[i] = ''
                        elif item == '[CLS]':
                            # text[i] = '\n\n'
                            text[i] = ''
                        elif item == '[SEP]':
                            # text[i] = '\n'
                            text[i] = ''
                    text = ''.join(text).replace('##', '').strip()
                    data.append(text[-80:])
            if generated == nsamples:
                break
        return data

