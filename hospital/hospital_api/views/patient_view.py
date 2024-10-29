from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from hospital.repository.repositories.repository_manager import RepositoryManager
from ..serializers.patient_serializer import PatientSerializer


class PatientList(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        patients = RepositoryManager().patients.get_all()
        serializer = PatientSerializer(patients, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            RepositoryManager().patients.create(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetail(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        return RepositoryManager().patients.get_by_id(id)

    def get(self, request, id, *args, **kwargs):
        patient = self.get_object(id)
        if patient is None:
            return Response({"detail": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
            patient = self.get_object(id)
            if patient is None:
                return Response({"detail": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = PatientSerializer(patient, data=request.data)
            if serializer.is_valid():
                RepositoryManager().patients.update(patient, **serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        patient = self.get_object(id)
        if patient is None:
            return Response({"detail": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)
        RepositoryManager().patients.delete(patient)
        return Response({"detail": "Patient was successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
