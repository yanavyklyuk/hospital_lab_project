from django.shortcuts import render


def home(request):
    return render(request, 'frontend/home_page/home_page.html')
