from rest_framework import serializers
from repository.models.appointment import Appointment
from hospital_api.serializers import DoctorSerializer, PatientSerializer, FavorSerializer
from repository.repositories.repository_manager import RepositoryManager


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=RepositoryManager().doctors.get_all(),
                                                   source='doctor', write_only=True, required=True)
    patient = PatientSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset=RepositoryManager().patients.get_all(),
                                                    source='patient', write_only=True, required=True)

    favor = FavorSerializer(read_only=True)
    favor_id = serializers.PrimaryKeyRelatedField(queryset=RepositoryManager().favors.get_all(),
                                                  source='favor', write_only=True, required=True)
    class Meta:
        model = Appointment
        fields = ['datetime_of_appointment', 'status', 'doctor', 'doctor_id', 'patient', 'patient_id', 'favor', 'favor_id']