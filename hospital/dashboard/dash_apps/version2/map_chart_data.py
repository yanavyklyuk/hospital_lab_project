import requests
import pandas as pd
from django.conf import settings

api_token = "0e6b59d6b34a0f9a9119ced567d72cf7190e9e60"
def get_disease_histories(api_token = "0e6b59d6b34a0f9a9119ced567d72cf7190e9e60"):
    api_url = "http://127.0.0.1:8000/hospital/disease_histories/"
    headers = {
        'Authorization': f'Token {api_token}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        appointments = response.json()
    else:
        appointments = []

    flattened = []
    for item in appointments:
        flattened_item = {
            'id': item['id'],
            'start_of_disease': item['start_of_disease'],
            'end_of_disease': item['end_of_disease'],
            'patient_country': item['patient']['country'],
            'doctor': item['doctor']['last_name'],
            'disease': item['disease'],
        }
        flattened.append(flattened_item)

    df = pd.DataFrame(flattened)
    df = df.filter(items=['patient_country', 'disease'])

    return df

def get_diseases(df):
    diseases = df['disease'].unique()
    disease_options = [{'label': disease, 'value': disease} for disease in diseases]
    return disease_options
