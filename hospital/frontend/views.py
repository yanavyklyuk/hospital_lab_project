import requests
from django.shortcuts import render
from django.conf import settings


def doctor_list(request):
    api_url = "http://127.0.0.1:8000/hospital/doctors/"

    response = requests.get(api_url)

    if response.status_code == 200:
        doctors = response.json()
    else:
        doctors = []
    return render(request, 'frontend/doctor_list.html', {'doctors': doctors})
