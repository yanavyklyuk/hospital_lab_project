import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def appointment_list(request):
    api_url = "http://127.0.0.1:8000/hospital/appointments/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('datetime_of_appointment', 'Datetime of appointment'),
        ('status', 'Status'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('favor', 'Favor'),
    ]

    if response.status_code == 200:
        appointments = response.json()
    else:
        appointments = []

    return render(request, 'frontend/appointment/appointment_list.html', {'appointments': appointments,
                                                                'fields': fields})


def appointment_detail(request, id):
    api_url = f"http://127.0.0.1:8000/hospital/appointments/{id}/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('datetime_of_appointment', 'Datetime of appointment'),
        ('status', 'Status'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('favor', 'Favor'),
    ]

    if response.status_code == 200:
        appointment = response.json()
    else:
        appointment = None

    return render(request, 'frontend/appointment/appointment_detail.html', {'appointment': appointment,
                                                                  'fields': fields})
