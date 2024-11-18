import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def patient_diseases_list(request, id=None):
    api_url = f"http://127.0.0.1:8000/hospital/patients/{id}/diseases_journal/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('start_of_disease', 'Start'),
        ('end_of_disease', 'End'),
        ('doctor', 'Doctor'),
        ('disease', 'Disease'),
    ]

    if response.status_code == 200:
        patient_diseases = response.json()
    else:
        patient_diseases = []

    return render(request, 'frontend/patient_diseases/patient_diseases_list.html',
                  {'patient_diseases': patient_diseases, 'fields': fields})
