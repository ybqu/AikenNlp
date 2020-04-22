from django.shortcuts import render

# Create your views here.
def website(request):
    if request.method == 'GET':
        return render(request, 'about/website.html')

def author(request):
    if request.method == 'GET':
        return render(request, 'about/author.html')