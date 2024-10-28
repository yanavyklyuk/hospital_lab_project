from rest_framework import serializers
from repository.models.doctor import Doctor
from .specialisation_serializer import SpecialisationSerializer


class DoctorSerializer(serializers.ModelSerializer):
    specialisation = SpecialisationSerializer

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'specialisation', 'practice_start_date']
