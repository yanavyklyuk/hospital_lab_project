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

    flattened = []
    for item in appointments:
        flattened_item = {
            'id': item['id'],
            'datetime_of_appointment': item['datetime_of_appointment'],
            'status': item['status'],
            'doctor': item['doctor']['last_name'],  # Припускаємо, що doctor також є вкладеним
            'patient': item['patient']['last_name'],  # Аналогічно для patient
            'favor_name': item['favor']['name'],  # Витягуємо name з вкладеного серіалізатора
            'favor_cost': item['favor']['cost'],  # Витягуємо cost з вкладеного серіалізатора
        }
        flattened.append(flattened_item)

    df = pd.DataFrame(flattened)
    df = df[df['status'] == 'happened']
    df = df.filter(items=['favor_name', 'favor_cost'])
    print(df.columns)

    return df