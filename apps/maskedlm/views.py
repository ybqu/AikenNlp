from django.shortcuts import render

# Create your views here.

def maskedlm(request):
    if request.method == 'GET':
        return render(request, 'maskedlm.html')
