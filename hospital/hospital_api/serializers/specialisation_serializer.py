from rest_framework import serializers
from repository.models.specialisation import Specialisation


class SpecialisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialisation
        fields = ['id', 'name']
