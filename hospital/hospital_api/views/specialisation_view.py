from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from repository.repositories.repository_manager import RepositoryManager
from ..serializers.specialisation_serializer import SpecialisationSerializer

class SpecialisationList(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        specialisations = RepositoryManager().specialisations.get_all()
        serializer = SpecialisationSerializer(specialisations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = SpecialisationSerializer(data=request.data)
        if serializer.is_valid():
            RepositoryManager().specialisations.create(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SpecialisationDetail(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        return RepositoryManager().specialisations.get_by_id(id)

    def get(self, request, id, *args, **kwargs):
        specialisation = self.get_object(id)
        if specialisation is None:
            return Response({"detail": "Specialisation not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SpecialisationSerializer(specialisation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        specialisation = self.get_object(id)
        if specialisation is None:
            return Response({"detail": "Specialisation not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = SpecialisationSerializer(specialisation, data=request.data)
        if serializer.is_valid():
            RepositoryManager().specialisations.update(specialisation, **serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        specialisation = self.get_object(id)
        if specialisation is None:
            return Response({"detail": "Specialisation not found."}, status=status.HTTP_404_NOT_FOUND)
        RepositoryManager().specialisations.delete(specialisation)
        return Response({"detail": "Specialisation was successfully deleted."}, status=status.HTTP_204_NO_CONTENT)