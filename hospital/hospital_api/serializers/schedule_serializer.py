from rest_framework import serializers

from repository.models.schedule import Schedule
from hospital_api.serializers import DoctorSerializer
from repository.repositories.repository_manager import RepositoryManager


class ScheduleSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset=RepositoryManager().doctors.get_all(), source='doctor',
                                                   write_only=True, required=True)

    class Meta:
        model = Schedule
        fields = ['day', 'doctor', 'doctor_id', 'start_time', 'end_time', 'minutes_per_patient', 'cabinet_number']
