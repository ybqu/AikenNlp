from django.shortcuts import render

# Create your views here.

def writeai(request):
    if request.method == 'GET':
        return render(request, 'writeai.html')
