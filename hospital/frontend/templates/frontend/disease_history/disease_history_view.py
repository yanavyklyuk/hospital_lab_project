import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def disease_history_list(request):
    api_url = "http://127.0.0.1:8000/hospital/disease_histories/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('start_of_disease', 'Start'),
        ('end_of_disease', 'End'),
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('disease', 'Disease'),
    ]

    if response.status_code == 200:
        disease_histories = response.json()
    else:
        disease_histories = []

    return render(request, 'frontend/disease_history/disease_history_list.html', {'disease_histories': disease_histories,
                                                                'fields': fields})


def disease_history_detail(request, id):
    api_url = f"http://127.0.0.1:8000/hospital/disease_histories/{id}/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('start_of_disease', 'Start'),
        ('end_of_disease', 'End'),
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('disease', 'Disease'),
    ]

    if response.status_code == 200:
        disease_history = response.json()
    else:
        disease_history = None

    return render(request, 'frontend/disease_history/disease_history_detail.html', {'disease_history': disease_history,
                                                                                    'fields': fields})


def disease_history_form(request, id=None):
    api_url = f"http://127.0.0.1:8000/hospital/disease_histories/{id}/" if id else "http://127.0.0.1:8000/hospital/disease_histories/"
    headers = {'Authorization': f'Token {settings.API_TOKEN}'}

    if request.method == "POST":
        data = {
            'start_of_disease': request.POST.get('start_of_disease'),
            'end_of_disease': request.POST.get('end_of_disease'),
            'patient_id': request.POST.get('patient_id'),
            'doctor_id': request.POST.get('doctor_id'),
            'disease_id': request.POST.get('disease_id'),
        }

        if id:
            response = requests.put(api_url, headers=headers, json=data)
        else:
            response = requests.post(api_url, headers=headers, json=data)

        if response.status_code in [200, 201]:
            return redirect(reverse('disease_history_list'))
        else:
            form_errors = response.json()
            return render(request, 'frontend/disease_history/disease_history_form.html',
                          {'form_errors': form_errors, 'id': id})

    disease_history = {}
    if id:
        response = requests.get(api_url, headers=headers)
        disease_history = response.json()
        if response.status_code != 200:
            return redirect(reverse('disease_history_list'))

    patients_response = requests.get("http://127.0.0.1:8000/hospital/patients/", headers=headers)
    patients = patients_response.json() if patients_response.status_code == 200 else []

    doctors_response = requests.get("http://127.0.0.1:8000/hospital/doctors/", headers=headers)
    doctors = doctors_response.json() if doctors_response.status_code == 200 else []

    diseases_response = requests.get("http://127.0.0.1:8000/hospital/diseases/", headers=headers)
    diseases = diseases_response.json() if diseases_response.status_code == 200 else []

    return render(request, 'frontend/disease_history/disease_history_form.html',
                  {'disease_history': disease_history,
                           'patients': patients,
                           'doctors': doctors,
                           'diseases': diseases})
