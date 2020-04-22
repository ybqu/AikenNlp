from django.shortcuts import render

# Create your views here.
def interpretation(request):
    """ 隐喻解释 """
    if request.method == 'GET':
        return render(request, 'metaphor/interpretation.html')
def generation(request):
    """ 隐喻生成 """
    if request.method == 'GET':
        return render(request, 'metaphor/generation.html')
def simile(request):
    """ 明喻提取 """
    if request.method == 'GET':
        return render(request, 'metaphor/simile.html')