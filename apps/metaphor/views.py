from django.shortcuts import render
from .MetaphorModel import showData

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
        print(target)
        print(source)

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
        attribute = request.POST.get('attribute')
        print(target)
        print(attribute)

def simile(request):
    """ 明喻提取 """
    if request.method == 'GET':
        return render(request, 'metaphor/simile.html')
    elif request.method == 'POST':
        sentence = request.POST.get('sentence')
    
    # print(sentence)