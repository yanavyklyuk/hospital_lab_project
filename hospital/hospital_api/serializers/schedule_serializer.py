from rest_framework import serializers
from repository.models.schedule import Schedule
from doctor_serializer import DoctorSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer

    class Meta:
        model = Schedule
        fields = ['id', 'day', 'doctor', 'start_time', 'end_time', 'cabinet_number']
