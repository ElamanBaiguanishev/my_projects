from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'test_app/index.html')


def about(request):
    return render(request, 'test_app/about.html')
