import requests
from django.shortcuts import render
from django.conf import settings


def specialisation_list(request):
    api_url = "http://127.0.0.1:8000/hospital/specialisations/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('name', 'Name'),
    ]

    if response.status_code == 200:
        specialisations = response.json()
    else:
        specialisations = []
    return render(request, 'frontend/specialisation/specialisation_list.html', {
        'specialisations': specialisations,
        'fields': fields
    })


def specialisation_detail(request, id):
    api_url = f"http://127.0.0.1:8000/hospital/specialisations/{id}/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('name', 'Name'),
    ]

    if response.status_code == 200:
        specialisation = response.json()
    else:
        specialisation = None

    return render(request, 'frontend/specialisation/specialisation_detail.html', {'specialisation': specialisation, 'fields': fields})
