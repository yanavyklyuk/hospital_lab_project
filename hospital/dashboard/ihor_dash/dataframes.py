import requests
import pandas as pd
from django.conf import settings
from datetime import datetime


def get_experience_dataframe(api_token):
    api_url = "http://127.0.0.1:8000/hospital/appointments/"
    headers = {
        'Authorization': f'Token {api_token}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        appointments = response.json()
    else:
        appointments = []

    flattened_appointments = []

    for item in appointments:
        practice_start_date = datetime.strptime(item['doctor']['practice_start_date'], '%Y-%m-%d')  # Припускаємо, що дата у форматі 'YYYY-MM-DD'
        current_date = datetime.now()

        years_of_experience = current_date.year - practice_start_date.year
        if (current_date.month, current_date.day) < (practice_start_date.month, practice_start_date.day):
            years_of_experience -= 1

        flattened_item = {
            'id': item['id'],
            'datetime_of_appointment': item['datetime_of_appointment'],
            'status': item['status'],
            'doctor_id': item['doctor']['id'],
            'experience': years_of_experience,
            'patient': item['patient']['last_name'],
            'favor_name': item['favor']['name'],
            'favor_cost': item['favor']['cost'],
        }

        flattened_appointments.append(flattened_item)

    df = pd.DataFrame(flattened_appointments)
    df = df[df['status'] == 'happened']

    appointment_counts = df.groupby('doctor_id').size().reset_index(name='appointment_count')
    df = df.merge(appointment_counts, on='doctor_id')

    experience_bins = [0, 5, 10, 15, float('inf')]
    experience_labels = ['0-5 years', '5-10 years', '10-15 years', '15+ years']
    df['experience_category'] = pd.cut(df['experience'], bins=experience_bins, labels=experience_labels, right=False)

    appointment_bins = [0, 5, 10, 20, 30, float('inf')]
    appointment_labels = ['0-5', '5-10', '10-20', '20-30', '30+']
    df['appointment_category'] = pd.cut(df['appointment_count'], bins=appointment_bins, labels=appointment_labels, right=False)

    grouped_df = df.groupby(['experience_category', 'appointment_category'], observed=False)['doctor_id'].nunique().reset_index(name='doctor_count')

    return grouped_df


def get_disease_history_seasons_dataframe(api_token):
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


def describe_to_table(df):
    if df.empty:
        return []

    description = df.describe()

    description_reset = description.reset_index()

    description_reset.columns = ['Statistic'] + list(description.columns)

    table_data = description_reset.to_dict('records')

    return table_data
