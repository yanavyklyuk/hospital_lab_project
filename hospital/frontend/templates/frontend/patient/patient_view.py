import requests
from django.shortcuts import render, redirect
from django.urls import reverse
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
        ('emergency_contact', 'Emergency Contact'),
    ]

    if response.status_code == 200:
        patient = response.json()
    else:
        patient = None

    return render(request, 'frontend/patient/patient_detail.html', {'patient': patient, 'fields': fields})

def patient_form(request, id=None):
    api_url = f"http://127.0.0.1:8000/hospital/patients/{id}/" if id else "http://127.0.0.1:8000/hospital/patients/"
    headers = {'Authorization': f'Token {settings.API_TOKEN}'}

    SEX = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    BLOOD_TYPES = [
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    if request.method == "POST":
        data = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "sex": request.POST.get("sex"),
            "date_birth": request.POST.get("date_birth"),
            "phone_number": request.POST.get("phone_number"),
            "country": request.POST.get("country"),
            "city": request.POST.get("city"),
            "street": request.POST.get("street"),
            "blood_type": request.POST.get("blood_type"),
            "insurance": request.POST.get("insurance"),
        }

        if id:
            response = requests.put(api_url, json=data, headers=headers)
        else:
            response = requests.post(api_url, json=data, headers=headers)

        if response.status_code in [200, 201]:
            return redirect(reverse('patient_list'))
        else:
            form_errors = response.json()
            return render(request, 'frontend/patient/patient_form.html',
                          {'form_errors': form_errors, 'id': id})
    patient = {}
    if id:
        response = requests.get(api_url, headers=headers)
        patient = response.json()
        if response.status_code != 200:
            return redirect(reverse('patient_list'))

    return render(request, 'frontend/patient/patient_form.html', {'patient': patient, 'SEX': SEX,
                                                                'BLOOD_TYPES': BLOOD_TYPES})
