from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from repository.repositories.repository_manager import RepositoryManager
from ..serializers.disease_history_serializer import DiseaseHistorySerializer


class DiseaseHistoryList(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        disease_histories = RepositoryManager().disease_histories.get_all()
        serializer = DiseaseHistorySerializer(disease_histories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DiseaseHistorySerializer(data=request.data)
        if serializer.is_valid():
            RepositoryManager().disease_histories.create(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiseaseHistoryDetail(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        return RepositoryManager().disease_histories.get_by_id(id)

    def get(self, request, id, *args, **kwargs):
        disease_history = self.get_object(id)
        if disease_history is None:
            return Response({"detail": "Disease history not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = DiseaseHistorySerializer(disease_history)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        disease_history = self.get_object(id)
        if disease_history is None:
            return Response({"detail": "Disease history not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DiseaseHistorySerializer(disease_history, data=request.data)
        if serializer.is_valid():
            RepositoryManager().disease_histories.update(disease_history, **serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        disease_history = self.get_object(id)
        if disease_history is None:
            return Response({"detail": "Disease_history not found."}, status=status.HTTP_404_NOT_FOUND)
        RepositoryManager().patients.delete(disease_history)
        return Response({"detail": "Disease history was successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
