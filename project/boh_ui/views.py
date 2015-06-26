from django.shortcuts import render


def index(request):
    return render(request, 'boh_ui/index.html')
