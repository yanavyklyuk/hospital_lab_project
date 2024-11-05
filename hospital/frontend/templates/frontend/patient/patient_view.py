import requests
from django.shortcuts import render
from django.conf import settings


def patient_list(request):
    api_url = "http://127.0.0.1:8000/hospital/patients/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('sex', 'Sex'),
        ('date_birth', 'Date of Birth'),
        ('phone_number', 'Phone Number'),
        ('blood_type', 'Blood Type'),
    ]

    if response.status_code == 200:
        patients = response.json()
    else:
        patients = []
    return render(request, 'frontend/patient/patient_list.html', {'patients': patients, 'fields': fields})


def patient_detail(request, id):
    api_url = f"http://127.0.0.1:8000/hospital/patients/{id}/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('sex', 'Sex'),
        ('date_birth', 'Date of Birth'),
        ('phone_number', 'Phone Number'),
        ('country', 'Country'),
        ('city', 'City'),
        ('street', 'Street'),
        ('blood_type', 'Blood Type'),
        ('insurance', 'Insurance'),
    ]

    if response.status_code == 200:
        patient = response.json()
    else:
        patient = None

    return render(request, 'frontend/patient/patient_detail.html', {'patient': patient, 'fields': fields})
