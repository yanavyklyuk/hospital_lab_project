from rest_framework import serializers
from repository.models.patient import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'sex', 'date_birth', 'phone_number', 'country', 'city', 'street',
                  'blood_type', 'insurance', 'emergency_contact']
        