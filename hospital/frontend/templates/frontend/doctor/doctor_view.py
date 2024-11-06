import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def doctor_list(request):
    api_url = "http://127.0.0.1:8000/hospital/doctors/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('specialisation', 'Specialisation'),
        ('phone_number', 'Phone Number')
    ]

    if response.status_code == 200:
        doctors = response.json()
    else:
        doctors = []

    return render(request, 'frontend/doctor/doctor_list.html', {'doctors': doctors, 'fields': fields})


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


def doctor_form(request, id=None):
    api_url = f"http://127.0.0.1:8000/hospital/doctors/{id}/" if id else "http://127.0.0.1:8000/hospital/doctors/"
    headers = {'Authorization': f'Token {settings.API_TOKEN}'}

    SEX = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    if request.method == "POST":
        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "sex": request.POST.get("sex"),
            "date_birth": request.POST.get("date_birth"),
            "phone_number": request.POST.get("phone_number"),
            "practice_start_date": request.POST.get("practice_start_date"),
            "education": request.POST.get("education"),
            "specialisation_id": request.POST.get("specialisation_id"),
        }

        if id:
            response = requests.put(api_url, json=data, headers=headers)
        else:
            response = requests.post(api_url, json=data, headers=headers)

        if response.status_code in [200, 201]:
            return redirect(reverse('doctor_list'))
        else:
            form_errors = response.json()
            return render(request, 'frontend/doctor/doctor_form.html',
                          {'form_errors': form_errors, 'id': id})
    doctor = {}
    if id:
        response = requests.get(api_url, headers=headers)
        doctor = response.json()
        if response.status_code != 200:
            return redirect(reverse('doctor_list'))

    specialisations_response = requests.get("http://127.0.0.1:8000/hospital/specialisations/", headers=headers)
    specialisations = specialisations_response.json() if specialisations_response.status_code == 200 else []

    return render(request, 'frontend/doctor/doctor_form.html', {'doctor': doctor,
                                                                'specialisations': specialisations, 'SEX': SEX})
