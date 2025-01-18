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


def appointment_form(request, id=None):
    api_url = f"http://127.0.0.1:8000/hospital/appointments/{id}/" if id else "http://127.0.0.1:8000/hospital/appointments/"
    headers = {'Authorization': f'Token {settings.API_TOKEN}'}

    STATUS = [
        ('scheduled', 'Scheduled'),
        ('happened', 'Happened'),
        ('cancelled', 'Cancelled')
    ]

    if request.method == "POST":
        data = {
            'datetime_of_appointment': request.POST.get('datetime_of_appointment'),
            'status': request.POST.get('status'),
            'doctor_id': request.POST.get('doctor_id'),
            'patient_id': request.POST.get('patient_id'),
            'favor_id': request.POST.get('favor_id'),
        }

        if id:
            response = requests.put(api_url, json=data, headers=headers)
        else:
            response = requests.post(api_url, json=data, headers=headers)

        if response.status_code in [200, 201]:
            return redirect(reverse('appointment_list'))
        else:
            try:
                form_errors = response.json()
                return render(request, 'frontend/appointment/appointment_form.html',
                          {'form_errors': form_errors, 'id': id})
            except:
                return render(request, 'frontend/error.html',)

    appointment = {}
    if id:
        response = requests.get(api_url, headers=headers)
        appointment = response.json()
        if response.status_code != 200:
            return redirect(reverse('appointment_list'))

    doctors_response = requests.get("http://127.0.0.1:8000/hospital/doctors/", headers=headers)
    doctors = doctors_response.json() if doctors_response.status_code == 200 else []

    patients_response = requests.get("http://127.0.0.1:8000/hospital/patients/", headers=headers)
    patients = patients_response.json() if patients_response.status_code == 200 else []

    favors_response = requests.get("http://127.0.0.1:8000/hospital/favors/", headers=headers)
    favors = favors_response.json() if favors_response.status_code == 200 else []

    return render(request, 'frontend/appointment/appointment_form.html', {'appointment': appointment,
                                                                          'doctors': doctors,
                                                                          'patients': patients,
                                                                          'favors': favors,
                                                                          'STATUS': STATUS})
