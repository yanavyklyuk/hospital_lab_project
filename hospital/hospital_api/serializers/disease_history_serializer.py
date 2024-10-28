from rest_framework import serializers
from repository.models.disease_history import DiseaseHistory
from hospital_api.serializers import context
from hospital_api.serializers import DoctorSerializer, PatientSerializer

class DiseaseHistorySerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only = True)
    patient_id = serializers.PrimaryKeyRelatedField(queryset = context().patients.get_all(),
                                                    source = 'patient', write_only = True, required =True)

    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(queryset = context().doctors.get_all(),
                                                   source = 'doctor', write_only=True, required=True)

    disease = serializers.SlugRelatedField(read_only=True, slug_field='name')
    disease_id = serializers.PrimaryKeyRelatedField(queryset=context().diseases.get_all(),
                                                    source='disease', write_only=True, required=True)

    class Meta:
        model = DiseaseHistory
        fields = ['start_of_disease', 'end_of_disease', 'patient', 'patient_id', 'doctor', 'doctor_id', 'disease', 'disease_id']