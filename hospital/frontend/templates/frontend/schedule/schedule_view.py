import requests
from django.shortcuts import render
from django.conf import settings


def schedule_list(request):
    api_url = "http://127.0.0.1:8000/hospital/schedules/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('day', 'Day'),
        ('doctor', 'Doctor'),
        ('start_time', 'Start Time'),
        ('end_time', 'End Time'),
        ('minutes_per_patient', 'Minutes per Patient'),
        ('cabinet_number', 'Cabinet Number'),
    ]

    if response.status_code == 200:
        schedules = response.json()
    else:
        schedules = []
    return render(request, 'frontend/schedule/schedule_list.html', {'schedules': schedules, 'fields': fields})


def schedule_detail(request, id):
    api_url = f"http://127.0.0.1:8000/hospital/schedules/{id}/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('day', 'Day'),
        ('doctor', 'Doctor'),
        ('doctor_id', 'Doctor ID'),
        ('start_time', 'Start Time'),
        ('end_time', 'End Time'),
        ('minutes_per_patient', 'Minutes per Patient'),
        ('cabinet_number', 'Cabinet Number'),
    ]

    if response.status_code == 200:
        schedule = response.json()
    else:
        schedule = None

    return render(request, 'frontend/schedule/schedule_detail.html', {'schedule': schedule, 'fields': fields})
