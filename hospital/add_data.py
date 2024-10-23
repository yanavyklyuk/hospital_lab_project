import os
import django
from repository.repositories.repository_manager import RepositoryManager


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()


def add_data():
    repo_manager = RepositoryManager()

    try:
        specialisations = ['Cardiologist', 'Surgeon', 'Dentist', 'Psychiatrist', 'Orthopedist']

        for name in specialisations:
            repo_manager.specialisations.create(name=name)

        print("Specialisation added successfully!")

    except Exception as e:(
        print(f"Error occurred: {e}"))

    try:
        doctor_data1 = {
            'first_name': 'John',
            'last_name': 'Doe',
            'sex': 'male',
            'date_birth': '1990-01-01',
            'phone_number': '+1 987654321',
            'practice_start_date': '2020-01-01',
            'specialisation': repo_manager.specialisations.get_by_id(1),
            'education': 'Harvard Medical School',
            'photo': None
        }

        doctor_data2 = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'sex': 'female',
            'date_birth': '1985-06-15',
            'phone_number': '+1 987754321',
            'practice_start_date': '2018-03-20',
            'specialisation': repo_manager.specialisations.get_by_id(2),
            'education': 'Stanford University School of Medicine',
            'photo': None
        }

        doctor_data3 = {
            'first_name': 'Michael',
            'last_name': 'Johnson',
            'sex': 'male',
            'date_birth': '1978-09-30',
            'phone_number': '+1 987654324',
            'practice_start_date': '2010-11-05',
            'specialisation': repo_manager.specialisations.get_by_id(3),
            'education': 'Johns Hopkins University',
            'photo': None
        }

        doctor_data4 = {
            'first_name': 'Emily',
            'last_name': 'Davis',
            'sex': 'female',
            'date_birth': '1992-02-22',
            'phone_number': '+1 987654325',
            'practice_start_date': '2021-07-15',
            'specialisation': repo_manager.specialisations.get_by_id(4),
            'education': 'Columbia University Vagelos College of Physicians and Surgeons',
            'photo': None
        }

        doctor_data5 = {
            'first_name': 'William',
            'last_name': 'Brown',
            'sex': 'male',
            'date_birth': '1980-12-12',
            'phone_number': '+1 987654326',
            'practice_start_date': '2015-05-10',
            'specialisation': repo_manager.specialisations.get_by_id(4),
            'education': 'Mayo Clinic Alix School of Medicine',
            'photo': None
        }

        doctors_data = [doctor_data1, doctor_data2, doctor_data3, doctor_data4, doctor_data5]

        for data in doctors_data:
            repo_manager.doctors.create(**data)

        print("Doctor added successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")

    try:
        diseases = ['Hernia', 'Appendicitis', 'Schizophrenia', 'Bipolar disorder', 'Hypertension', 'Dental caries',
                    'Scoliosis']

        for name in diseases:
            repo_manager.diseases.create(name=name)

        print("Diseases added successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")

    try:
        favor_data1 = {
            'name': 'Consultation',
            'cost': 750
        }

        favor_data2 = {
            'name': 'Ultrasound',
            'cost': 600
        }

        favor_data3 = {
            'name': 'Computed Tomography',
            'cost': 1300
        }

        favors_data = [favor_data1, favor_data2, favor_data3]

        for data in favors_data:
            repo_manager.favors.create(**data)

        print("Favors added successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")

    try:
        patient_data1 = {
            'first_name': 'Lucy',
            'last_name': 'Scott',
            'sex': 'female',
            'date_birth': '1999-04-22',
            'phone_number': '+1 154826359',
            'country': 'USA',
            'city': 'New York City',
            'street': 'Broadway',
            'blood_type': 'A+',
            'insurance': True,
            'emergency_contact': '+1 111025784'
        }

        patient_data2 = {
            'first_name': 'Michael',
            'last_name': 'Johnson',
            'sex': 'male',
            'date_birth': '1985-11-15',
            'phone_number': '+1 415263741',
            'country': 'USA',
            'city': 'San Francisco',
            'street': 'Market Street',
            'blood_type': 'O-',
            'insurance': False,
            'emergency_contact': '+1 223145678'
        }

        patient_data3 = {
            'first_name': 'Emily',
            'last_name': 'Davis',
            'sex': 'female',
            'date_birth': '1978-06-10',
            'phone_number': '+1 345278956',
            'country': 'Canada',
            'city': 'Toronto',
            'street': 'Queen Street',
            'blood_type': 'B+',
            'insurance': True,
            'emergency_contact': '+1 678543210'
        }

        patients_data = [patient_data1, patient_data2, patient_data3]

        for data in patients_data:
            repo_manager.patients.create(**data)

        print("Patients added successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")

    try:
        disease_history_data1 = {
            'start_of_disease': '2024-07-11',
            'end_of_disease': '2024-07-21',
            'patient': repo_manager.patients.get_by_id(1),
            'doctor': repo_manager.doctors.get_by_id(2),
            'disease': repo_manager.diseases.get_by_id(1)
        }

        disease_history_data2 = {
            'start_of_disease': '2024-08-10',
            'end_of_disease': None,
            'patient': repo_manager.patients.get_by_id(1),
            'doctor': repo_manager.doctors.get_by_id(5),
            'disease': repo_manager.diseases.get_by_id(4)
        }

        disease_history_data3 = {
            'start_of_disease': '2024-09-01',
            'end_of_disease': '2024-09-03',
            'patient': repo_manager.patients.get_by_id(2),
            'doctor': repo_manager.doctors.get_by_id(2),
            'disease': repo_manager.diseases.get_by_id(2)
        }

        disease_history_data4 = {
            'start_of_disease': '2024-09-10',
            'end_of_disease': '2024-09-24',
            'patient': repo_manager.patients.get_by_id(3),
            'doctor': repo_manager.doctors.get_by_id(3),
            'disease': repo_manager.diseases.get_by_id(6)
        }

        disease_history_data5 = {
            'start_of_disease': '2024-10-10',
            'end_of_disease': None,
            'patient': repo_manager.patients.get_by_id(3),
            'doctor': repo_manager.doctors.get_by_id(5),
            'disease': repo_manager.diseases.get_by_id(3)
        }

        disease_histories_data = [disease_history_data1, disease_history_data2, disease_history_data3,
                                  disease_history_data4, disease_history_data5]

        for data in disease_histories_data:
            repo_manager.disease_histories.create(**data)

        print("Disease histories added successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")

    try:
        schedule_data1 = {
            'day': 'Monday',
            'start_time': '09:00:00',
            'end_time': '17:00:00',
            'minutes_per_patient': 45,
            'cabinet_number': 107,
            'doctor': repo_manager.doctors.get_by_id(1)
        }

        schedule_data2 = {
            'day': 'Tuesday',
            'start_time': '10:00:00',
            'end_time': '13:00:00',
            'minutes_per_patient': 60,
            'cabinet_number': 314,
            'doctor': repo_manager.doctors.get_by_id(3)
        }

        schedule_data3 = {
            'day': 'Monday',
            'start_time': '09:00:00',
            'end_time': '16:00:00',
            'minutes_per_patient': 45,
            'cabinet_number': 117,
            'doctor': repo_manager.doctors.get_by_id(2)
        }

        schedules_data = [schedule_data1, schedule_data2, schedule_data3]

        for data in schedules_data:
            repo_manager.schedules.create(**data)

    except Exception as e:
        print(f"Error occurred: {e}")

    try:
        appointment_data1 = {
            'datetime_of_appointment': '2024-07-11 09:00:00',
            'status': 'happened',
            'doctor': repo_manager.doctors.get_by_id(2),
            'patient': repo_manager.patients.get_by_id(1),
            'favor': repo_manager.favors.get_by_id(2)
        }

        appointment_data2 = {
            'datetime_of_appointment': '2024-08-10 10:30:00',
            'status': 'cancelled',
            'doctor': repo_manager.doctors.get_by_id(5),
            'patient': repo_manager.patients.get_by_id(1),
            'favor': repo_manager.favors.get_by_id(1)
        }

        appointment_data3 = {
            'datetime_of_appointment': '2024-09-01 10:00:00',
            'status': 'happened',
            'doctor': repo_manager.doctors.get_by_id(2),
            'patient': repo_manager.patients.get_by_id(2),
            'favor': repo_manager.favors.get_by_id(3)
        }

        appointment_data4 = {
            'datetime_of_appointment': '2024-09-10 14:15:00',
            'status': 'happened',
            'doctor': repo_manager.doctors.get_by_id(3),
            'patient': repo_manager.patients.get_by_id(3),
            'favor': repo_manager.favors.get_by_id(1)
        }

        appointment_data5 = {
            'datetime_of_appointment': '2024-10-10 09:45:00',
            'status': 'happened',
            'doctor': repo_manager.doctors.get_by_id(5),
            'patient': repo_manager.patients.get_by_id(3),
            'favor': repo_manager.favors.get_by_id(1)
        }

        appointments_data = [appointment_data1, appointment_data2, appointment_data3,
                             appointment_data4, appointment_data5]

        for data in appointments_data:
            repo_manager.appointments.create(**data)

    except Exception as e:
        print(f"Error occurred: {e}")


if __name__ == '__main__':
    add_data()
