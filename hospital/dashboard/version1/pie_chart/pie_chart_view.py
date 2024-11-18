import requests
import pandas as pd
from django.conf import settings


def get_appointments():
    api_url = "http://127.0.0.1:8000/hospital/appointments/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        appointments = response.json()
    else:
        appointments = []

    df = pd.DataFrame(appointments)
    df = df[df['status'] == 'happened']
    df = df.filter(items=['name', 'cost'])

    return df