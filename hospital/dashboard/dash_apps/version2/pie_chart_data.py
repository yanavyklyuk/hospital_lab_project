import requests
import pandas as pd

def get_appointments(api_token='0e6b59d6b34a0f9a9119ced567d72cf7190e9e60'):
    api_url = "http://127.0.0.1:8000/hospital/appointments/"
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
            'datetime_of_appointment': item['datetime_of_appointment'],
            'status': item['status'],
            'doctor': item['doctor']['last_name'],
            'patient': item['patient']['last_name'],
            'favor_name': item['favor']['name'],
            'favor_cost': item['favor']['cost'],
        }
        flattened.append(flattened_item)

    df = pd.DataFrame(flattened)
    df = df[df['status'] == 'happened']
    df = df.filter(items=['favor_name', 'favor_cost'])
    df['favor_cost'] = df['favor_cost'].astype(float)


    return df