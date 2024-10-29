from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from hospital.repository.repositories.repository_manager import RepositoryManager
from ..serializers.doctor_serializer import DoctorSerializer

class DoctorList(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        doctors = RepositoryManager().doctors.get_all()
        serializer = DoctorSerializer(doctors, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            RepositoryManager().doctors.create(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorDetail(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        return RepositoryManager().doctors.get_by_id(id)

    def get(self, request, id, *args, **kwargs):
        doctor = self.get_object(id)
        if doctor is None:
            return Response({"detail": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        doctor = self.get_object(id)
        if doctor is None:
            return Response({"detail": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            RepositoryManager().doctors.update(doctor, **serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        doctor = self.get_object(id)
        if doctor is None:
            return Response({"detail": "Doctor not found."}, status=status.HTTP_404_NOT_FOUND)
        RepositoryManager().doctors.delete(doctor)
        return Response({"detail": "Doctor was successfully deleted."}, status=status.HTTP_204_NO_CONTENT)