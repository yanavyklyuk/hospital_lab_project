from rest_framework import serializers
from repository.models.favor import Favor


class FavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favor
        fields = ['name', 'cost']
