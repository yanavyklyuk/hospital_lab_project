from ..repositories.favor_repository import FavorRepository
from ..repositories.disease_repository import DiseaseRepository
from ..repositories.doctor_repository import DoctorRepository
from ..repositories.appointment_repository import AppointmentRepository
from ..repositories.disease_history_repository import DiseaseHistoryRepository
from ..repositories.patient_repository import PatientRepository
from ..repositories.schedule_repository import ScheduleRepository
from ..repositories.specialisation_repository import SpecialisationRepository


class RepositoryManager:
    def __init__(self):
        self.appointments = AppointmentRepository()
        self.diseases = DiseaseRepository()
        self.disease_histories = DiseaseHistoryRepository()
        self.doctors = DoctorRepository()
        self.favors = FavorRepository()
        self.patients = PatientRepository()
        self.schedule = ScheduleRepository()
        self.specialisation = SpecialisationRepository()
