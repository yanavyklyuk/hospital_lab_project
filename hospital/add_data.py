import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

from repository.repositories.repository_manager import RepositoryManager

def add_data():
    repo_manager = RepositoryManager()

    try:
        specialisations = ['Cardiologist', 'Surgeon', 'Dentist', 'Psychiatrist', 'Orthopedist']

        for name in specialisations:
            repo_manager.specialisations.create(name=name)

        print("Specialisation added successfully!")

    except Exception as e:(
        print(f"Error ocurred: {e}"))

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
        print(f"Error ocurred: {e}")

    try:
        diseases = ['Hernia', 'Appendicitis', 'Schizophrenia', 'Bipolar disorder', 'Hypertension', 'Dental caries',
                    'Scoliosis']

        for name in diseases:
            repo_manager.diseases.create(name=name)

        print("Specialisation added successfully!")

    except Exception as e:
       print(f"Error ocurred: {e}")


if __name__ == '__main__':
    add_data()