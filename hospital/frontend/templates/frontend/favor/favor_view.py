import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def favor_list(request):
    api_url = "http://127.0.0.1:8000/hospital/favors/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('name', 'Name'),
        ('cost', 'Cost'),
    ]

    if response.status_code == 200:
        favors = response.json()
    else:
        favors = []
    return render(request, 'frontend/favor/favor_list.html', {'favors': favors, 'fields': fields})


def favor_detail(request, id):
    api_url = f"http://127.0.0.1:8000/hospital/favors/{id}/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    fields = [
        ('name', 'Name'),
        ('cost', 'Cost'),
    ]

    if response.status_code == 200:
        favor = response.json()
    else:
        favor = None

    return render(request, 'frontend/favor/favor_detail.html', {'favor': favor, 'fields': fields})


def favor_form(request, id=None):
    api_url = f"http://127.0.0.1:8000/hospital/favors/{id}/" if id else "http://127.0.0.1:8000/hospital/favors/"
    headers = {'Authorization': f'Token {settings.API_TOKEN}'}

    if request.method == 'POST':
        data = {
            'name': request.POST.get('name'),
            'cost': request.POST.get('cost'),
        }
        if id:
            response = requests.put(api_url, headers=headers, json=data)
        else:
            response = requests.post(api_url, headers=headers, json=data)

        if response.status_code in [200, 201]:
            return redirect(reverse('favor_list'))
        else:
            form_errors = response.json()
            return render(request, 'frontend/favor/favor_form.html',
                          {'form_errors': form_errors, 'id': id})

    favor = {}
    if id:
        response = requests.get(api_url, headers=headers)
        favor = response.json()
        if response.status_code != 200:
            return redirect(reverse('favor_list'))

    return render(request, 'frontend/favor/favor_form.html', {'favor': favor})


def favor_delete(request, id):
    api_url = f"http://127.0.0.1:8000/hospital/favors/{id}/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    if request.method == "POST":
        response = requests.delete(api_url, headers=headers)

        if response.status_code == 204:
            return redirect(reverse('doctor_list'))
        else:
            return render(request, 'frontend/favor/favor_list.html', {
                'error_message': 'Failed to delete the favor. Please try again.'
            })

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        favor = response.json()
    else:
        favor = None

    return render(request, 'frontend/favor/favor_delete.html', {
        'favor': favor
    })
