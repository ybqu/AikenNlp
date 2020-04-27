import config
import torch
from django.db import models
from .MetaphorModel.main import METAPHOR_INTERPRET, METAPHOR_GENERATE
from util import Util

# Create your models here.
def ouput_pred(sentence, preds, label_map):
    """Output the preds labels."""

    id2label = dict(zip(label_map.values(), label_map.keys()))
    pred_labels = [id2label[p] for p in preds[0][1:len(sentence) + 1]]
    return pred_labels

class Interpretation(models.Model):
    @staticmethod
    def interprete(target, source):
        attribution, interpretation = METAPHOR_INTERPRET.metaphor_interpret(target, source)
        data_list = []
        for p, s in zip(attribution, interpretation):
            data = {'target': target, 'source': source, 'attribution': p, 'interpretation': s}
            data_list.append(data)
        return data_list

class Generation(models.Model):
    @staticmethod
    def generation(target, attribution):
        sources, sentences = METAPHOR_GENERATE.metaphor_generate(target, attribution)

        data_list = []
        for s, sent in zip(sources, sentences):
            data = {'target': target, 'attribution': attribution, 'source': s, 'sentences': sent}
            data_list.append(data)
        
        return data_list

class Simile(models.Model):
    @staticmethod
    def simile(sentence):
        _, label_map = Util.metaphor_label()

        device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
        tokenizer = config.SIMILE_TOKENIZER
        model = config.SIMILE_MODEL

        model.to(device)
        input_ids = torch.tensor(tokenizer.encode(sentence, add_special_tokens=True)).unsqueeze(0)
        segment_ids = torch.tensor([0] * len(input_ids[0]))
        input_mask = torch.tensor([1] * len(input_ids[0])).unsqueeze(0)

        model.eval()

        input_ids = input_ids.to(device)
        input_mask = input_mask.to(device)
        segment_ids = segment_ids.to(device)

        pred = model(input_ids, segment_ids, input_mask)

        return ouput_pred(sentence, pred, label_map)