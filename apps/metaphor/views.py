from django.shortcuts import render, HttpResponse
from .MetaphorModel import showData
from .models import Interpretation, Generation
import sys
import json

sys.path.append('../../')
from util import Util

# Create your views here.
def interpretation(request):
    """ 隐喻解释 """
    if request.method == 'GET':
        target_list, source_list, attribution_list = showData.get_entities_properties()
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
        target_list, source_list, attribution_list = showData.get_entities_properties()
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
        return render(request, 'metaphor/simile.html')
    elif request.method == 'POST':
        sentence = request.POST.get('sentence')

        data = []

    return HttpResponse(json.dumps(Util.returnData(0, '', len(data), data)))
    
    # print(sentence)