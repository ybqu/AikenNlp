from django.shortcuts import render, HttpResponse
from .MetaphorModel import getMData
from .SimileExtraction import getSData
from .models import Interpretation, Generation, Simile
import sys
import json

from util import Util

def get_simile(sentence, pred_labels):
    source_labels = {"ss": 1, "sb": 2, "si": 3, "se": 4}
    target_labels = {"ts": 1, "tb": 2, "ti": 3, "te": 4}
    ap_labels = {"aps": 1, "apb": 2, "api": 3, "ape": 4}
    vp_labels = {"vps": 1, "vpb": 2, "vpe": 3, "vpi": 4}

    source_words = []
    target_words = []
    ap_words = []
    vp_words = []

    for i, s in enumerate(sentence):
        if pred_labels[i] in source_labels:
            source_words.append(i)
        elif pred_labels[i] in target_labels:
            target_words.append(i)
        elif pred_labels[i] in ap_labels:
            ap_words.append(i)
        elif pred_labels[i] in vp_labels:
            vp_words.append(i)
    
    return {
        'sentence' : sentence,
        'target' : target_words,
        'source' : source_words,
        'adj' : ap_words,
        'verb' : vp_words
    }


# Create your views here.
def interpretation(request):
    """ 隐喻解释 """
    if request.method == 'GET':
        target_list, source_list, attribution_list = getMData.get_entities_properties()
        return render(request, 'metaphor/interpretation.html', {
            'targets':target_list
            , 'sources':source_list
            })
    elif request.method == 'POST':
        target = request.POST.get('target')
        source = request.POST.get('source')

        data = Interpretation.interprete(target, source)

        return HttpResponse(json.dumps(Util.returnData(0, '', len(data), data)))

def generation(request):
    """ 隐喻生成 """
    if request.method == 'GET':
        target_list, source_list, attribution_list = getMData.get_entities_properties()
        return render(request, 'metaphor/generation.html', {
            'targets':target_list
            , 'attributions':attribution_list
        })
    elif request.method == 'POST':
        target = request.POST.get('target')
        attribution = request.POST.get('attribution')

        data = Generation.generation(target, attribution)
        return HttpResponse(json.dumps(Util.returnData(0, '', len(data), data)))

def simile(request):
    """ 明喻提取 """
    if request.method == 'GET':
        sentence_label, sentences, labels = getSData.get_sentences()
        return render(request, 'metaphor/simile.html', {
            'sentences': sentences
        })
    elif request.method == 'POST':
        sentence = request.POST.get('sentence')

        pred_labels = Simile.simile(sentence)

        data = get_simile(sentence, pred_labels)

        return HttpResponse(json.dumps(Util.returnData(0, '', len(data), data)))