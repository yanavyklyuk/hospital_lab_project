import requests
from django.shortcuts import render
from django.conf import settings


def favor_list(request):
    api_url = "http://127.0.0.1:8000/hospital/favors/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('name', 'Name'),
        ('cost', 'Cost'),
    ]

    if response.status_code == 200:
        favors = response.json()
    else:
        favors = []
    return render(request, 'frontend/favor/favor_list.html', {'favors': favors, 'fields': fields})


def favor_detail(request, id):
    api_url = f"http://127.0.0.1:8000/hospital/favors/{id}/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('name', 'Name'),
        ('cost', 'Cost'),
    ]

    if response.status_code == 200:
        favor = response.json()
    else:
        favor = None

    return render(request, 'frontend/favor/favor_detail.html', {'favor': favor, 'fields': fields})
