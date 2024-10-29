from rest_framework import serializers
from repository.models.doctor import Doctor
from repository.repositories.repository_manager import RepositoryManager


class DoctorSerializer(serializers.ModelSerializer):
    specialisation = serializers.SlugRelatedField(read_only=True, slug_field='name')
    specialisation_id = serializers.PrimaryKeyRelatedField(queryset=RepositoryManager().specialisations.get_all(),
                                                           source='specialisation', write_only=True, required=True)

    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'sex', 'date_birth', 'phone_number', 'practice_start_date',
                  'specialisation', 'specialisation_id','education']