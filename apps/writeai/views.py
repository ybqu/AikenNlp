import json
import sys
from .models import Writeai
from django.shortcuts import render, HttpResponse

# Create your views here.
sys.path.append('../../')
from util import Util

def writeai(request):
    if request.method == 'GET':
        return render(request, 'textgeneration/writeai.html')
    elif request.method == 'POST':
        corpus = request.POST.get('corpus')
        prompt = request.POST.get('prompt')

        result = Writeai.generate(prefix=prompt, corpus = corpus, length=80)

        return HttpResponse(json.dumps(Util.return_data(0, '', len(result), result)))
