import json
from django.shortcuts import render, HttpResponse
from .models import Bert_Masked

# Create your views here.

def maskedlm(request):
    if request.method == 'GET':
        return render(request, 'maskedlm.html')
    elif request.method == 'POST':
        language = request.POST.get('language')
        sentence = request.POST.get('sentence')

        result = Bert_Masked.get_prediction(language, sentence)

        return HttpResponse(json.dumps({
            'code': 0,
            'msg': '',
            'count': result[1],
            'data': result[0]
        }))
