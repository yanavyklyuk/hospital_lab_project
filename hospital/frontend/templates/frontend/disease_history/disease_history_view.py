import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def disease_history_list(request):
    api_url = "http://127.0.0.1:8000/hospital/disease_histories/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('start_of_disease', 'Start'),
        ('end_of_disease', 'End'),
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('disease', 'Disease'),
    ]

    if response.status_code == 200:
        disease_histories = response.json()
    else:
        disease_histories = []

    return render(request, 'frontend/disease_history/disease_history_list.html', {'disease_histories': disease_histories,
                                                                'fields': fields})


def disease_history_detail(request, id):
    api_url = f"http://127.0.0.1:8000/hospital/disease_histories/{id}/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('start_of_disease', 'Start'),
        ('end_of_disease', 'End'),
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('disease', 'Disease'),
    ]

    if response.status_code == 200:
        disease_history = response.json()
    else:
        disease_history = None

    return render(request, 'frontend/disease_history/disease_history_detail.html', {'disease_history': disease_history,
                                                                                    'fields': fields})

