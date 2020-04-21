import json
from .models import Writeai
from django.shortcuts import render, HttpResponse

# Create your views here.

def writeai(request):
    if request.method == 'GET':
        return render(request, 'writeai.html')
    elif request.method == 'POST':
        corpus = request.POST.get('corpus')
        prompt = request.POST.get('prompt')

        result = Writeai.generate(prefix=prompt, corpus = corpus, length=80)

        return HttpResponse(json.dumps({
            'code': 0,
            'msg': '',
            'count': len(result),
            'data': result
        }))
