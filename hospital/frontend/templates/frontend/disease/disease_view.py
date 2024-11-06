import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def disease_list(request):
    api_url = "http://127.0.0.1:8000/hospital/diseases/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('name', 'Name')
    ]

    if response.status_code == 200:
        diseases = response.json()
    else:
        diseases = []

    return render(request, 'frontend/disease/disease_list.html', {'diseases': diseases, 'fields': fields})


def disease_detail(request, id):
    api_url = f"http://127.0.0.1:8000/hospital/diseases/{id}/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('name', 'Name')
    ]

    if response.status_code == 200:
        disease = response.json()
    else:
        disease = None

    return render(request, 'frontend/disease/disease_detail.html', {'disease': disease, 'fields': fields})