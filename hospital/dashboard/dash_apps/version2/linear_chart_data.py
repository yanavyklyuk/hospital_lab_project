import requests
import pandas as pd
from datetime import datetime
from django.conf import settings

api_token = "0e6b59d6b34a0f9a9119ced567d72cf7190e9e60"
def get_disease_history_seasons_dataframe(api_token = "0e6b59d6b34a0f9a9119ced567d72cf7190e9e60"):
    api_url = "http://127.0.0.1:8000/hospital/disease_histories/"

    headers = {
        'Authorization': f'Token {api_token}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        diseases = response.json()
    else:
        diseases = []

    flattened_diseases = []

    for item in diseases:
        start_date = datetime.strptime(item['start_of_disease'], '%Y-%m-%d')
        if item['end_of_disease'] is None:
            continue

        end_date = datetime.strptime(item['end_of_disease'], '%Y-%m-%d')

        duration = (end_date - start_date).days

        start_month = start_date.month

        flattened_item = {
            'id': item['id'],
            'start_of_disease': start_date,
            'disease': item['disease'],
            'duration': duration,
            'start_month': start_month
        }

        flattened_diseases.append(flattened_item)

    df = pd.DataFrame(flattened_diseases)

    return df

def get_diseases_l(df):
    diseases = df['disease'].unique()
    disease_options = [{'label': disease, 'value': disease} for disease in diseases]
    return disease_options

def get_years_l(df):
    pass