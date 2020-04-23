import json
import sys
from django.shortcuts import render, HttpResponse
from .models import Bert_Masked

# Create your views here.
sys.path.append('../../')
from util import Util

def maskedlm(request):
    if request.method == 'GET':
        return render(request, 'others/maskedlm.html')
    elif request.method == 'POST':
        language = request.POST.get('language')
        sentence = request.POST.get('sentence')

        result = Bert_Masked.get_prediction(language, sentence)

        return HttpResponse(json.dumps(Util.returnData(0, '', result[1], result[0])))
