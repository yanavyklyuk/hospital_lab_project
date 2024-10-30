from rest_framework import serializers
from repository.models.disease_history import DiseaseHistory
from repository.models.doctor import Doctor


class PatientDiseaseSerializer(serializers.ModelSerializer):

    class ShortDoctorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Doctor
            fields = ['first_name', 'last_name', 'phone_number']

    doctor = ShortDoctorSerializer(read_only=True)
    disease = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = DiseaseHistory
        fields = ['start_of_disease', 'end_of_disease', 'doctor', 'disease']
