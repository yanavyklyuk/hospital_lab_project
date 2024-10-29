from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from hospital.repository.repositories.repository_manager import RepositoryManager
from ..serializers.schedule_serializer import ScheduleSerializer

class ScheduleList(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        schedules = RepositoryManager().schedules.get_all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            RepositoryManager().schedules.create(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleDetail(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        return RepositoryManager().schedules.get_by_id(id)

    def get(self, request, id, *args, **kwargs):
        schedule = self.get_object(id)
        if schedule is None:
            return Response({"detail": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        schedule = self.get_object(id)
        if schedule is None:
            return Response({"detail": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            RepositoryManager().schedules.update(schedule, **serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        schedule = self.get_object(id)
        if schedule is None:
            return Response({"detail": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)
        RepositoryManager().schedules.delete(schedule)
        return Response({"detail": "Schedule was successfully deleted."}, status=status.HTTP_204_NO_CONTENT)