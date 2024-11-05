import requests
from django.shortcuts import render
from django.conf import settings


def doctor_list(request):
    api_url = "http://127.0.0.1:8000/hospital/doctors/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        doctors = response.json()
    else:
        doctors = []
    return render(request, 'frontend/doctor/doctor_list.html', {'doctors': doctors})

def doctor_detail(request, id):
    api_url = f"http://127.0.0.1:8000/hospital/doctors/{id}/"
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
        ('practice_start_date', 'Practice Start Date'),
        ('specialisation', 'Specialisation'),
        ('education', 'Education'),
    ]

    if response.status_code == 200:
        doctor = response.json()
    else:
        doctor = None

    return render(request, 'frontend/doctor/doctor_detail.html', {'doctor': doctor, 'fields': fields})
