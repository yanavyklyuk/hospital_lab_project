from rest_framework import serializers

from repository.models.schedule import Schedule


class DoctorScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ['day', 'start_time', 'end_time', 'cabinet_number']
