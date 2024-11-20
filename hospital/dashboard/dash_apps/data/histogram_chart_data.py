import requests
import pandas as pd
from django.conf import settings


def get_disease_histories_h():
    api_url = "http://127.0.0.1:8000/hospital/disease_histories/"
    headers = {
        'Authorization': f'Token {settings.API_TOKEN}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        appointments = response.json()
    else:
        appointments = []

    flattened = []
    now = pd.to_datetime('today')
    for item in appointments:
        flattened_item = {
            'id': item['id'],
            'start_of_disease': item['start_of_disease'],
            'end_of_disease': item['end_of_disease'] if item['end_of_disease'] else None,
            'patient_db': item['patient']['date_birth'],
            'doctor': item['doctor']['last_name'],
            'disease': item['disease'],
        }
        flattened.append(flattened_item)

    df = pd.DataFrame(flattened)
    df = df[df['end_of_disease'].notna()]
    df['patient_db'] = pd.to_datetime(df['patient_db'], errors='coerce')
    df['end_of_disease'] = pd.to_datetime(df['end_of_disease'], errors='coerce')
    df['start_of_disease'] = pd.to_datetime(df['start_of_disease'], errors='coerce')
    df['patient_age'] = (now - df['patient_db']).dt.days // 365
    df['duration'] = (df['end_of_disease'] - df['start_of_disease']).dt.days
    df = df.filter(items=['patient_age', 'disease', 'duration'])

    return df

def get_diseases_h(df):
    diseases = df['disease'].unique()
    disease_options = [{'label': disease, 'value': disease} for disease in diseases]
    return disease_options
