from rest_framework import serializers
from repository.models.patient import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'blood_type', 'insurance']
        