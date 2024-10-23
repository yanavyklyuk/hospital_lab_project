import os
import django
from repository.repositories.repository_manager import RepositoryManager


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()


def get_data():
    repo_manager = RepositoryManager()
    print('Specialisation with ID 1: ')
    print(repo_manager.specialisations.get_by_id(1))
    print('All specialisations: ')
    print(repo_manager.specialisations.get_all())

    print('Doctor with ID 1: ')
    print(repo_manager.doctors.get_by_id(1))
    print('Doctor with ID 6: ')
    print(repo_manager.doctors.get_by_id(6))
    print('All doctors: ')
    print(repo_manager.doctors.get_all())

    print('Disease with ID 1: ')
    print(repo_manager.diseases.get_by_id(2))
    print('All diseases: ')
    print(repo_manager.diseases.get_all())

    print('Patient with ID 1: ')
    print(repo_manager.patients.get_by_id(1))
    print('Patient with ID 6: ')
    print(repo_manager.patients.get_by_id(6))
    print('All patients: ')
    print(repo_manager.patients.get_all())


if __name__ == '__main__':
    get_data()