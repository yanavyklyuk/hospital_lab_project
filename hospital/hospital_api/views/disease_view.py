from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from hospital.repository.repositories.repository_manager import RepositoryManager
from ..serializers.disease_serializer import DiseaseSerializer


class DiseaseList(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        diseases = RepositoryManager().diseases.get_all()
        serializer = DiseaseSerializer(diseases, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DiseaseSerializer(data=request.data)
        if serializer.is_valid():
            RepositoryManager().diseases.create(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DiseaseDetail(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        return RepositoryManager().diseases.get_by_id(id)

    def get(self, request, id, *args, **kwargs):
        disease = self.get_object(id)
        if disease is None:
            return Response({"detail": "Disease not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DiseaseSerializer(disease)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        disease = self.get_object(id)
        if disease is None:
            return Response({"detail": "Disease not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DiseaseSerializer(disease, data=request.data)
        if serializer.is_valid():
            RepositoryManager().diseases.update(disease, **serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        disease = self.get_object(id)
        if disease is None:
            return Response({"detail": "Disease not found."}, status=status.HTTP_404_NOT_FOUND)
        RepositoryManager().diseases.delete(disease)
        return Response({"detail": "Disease was successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
