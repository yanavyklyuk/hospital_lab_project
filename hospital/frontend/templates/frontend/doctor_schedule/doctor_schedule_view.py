import requests
from django.shortcuts import render
from django.conf import settings


def doctor_schedule_list(request, id=None):
    api_url = f"http://127.0.0.1:8000/hospital/doctors/{id}/schedules"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('day', 'Day'),
        ('start_time', 'Start Time'),
        ('end_time', 'End Time'),
        ('cabinet_number', 'Cabinet Number'),
    ]

    if response.status_code == 200:
        doctor_schedules = response.json()
    else:
        doctor_schedules = []
    return render(request, 'frontend/doctor_schedule/doctor_schedule_list.html', {'doctor_schedules': doctor_schedules, 'fields': fields})