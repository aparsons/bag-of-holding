from django.shortcuts import render


def index(request):
    return render(request, 'pearson/pages/index.html', {
        'active_top': 'home'
    })
