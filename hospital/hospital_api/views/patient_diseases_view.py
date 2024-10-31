from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from repository.repositories.repository_manager import RepositoryManager
from ..serializers.patient_diseases_serializer import PatientDiseaseSerializer


class PatientDiseasesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, patient_id, *args, **kwargs):
        diseases = RepositoryManager().disease_histories.get_by_patient(patient_id)
        serializer = PatientDiseaseSerializer(diseases, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
