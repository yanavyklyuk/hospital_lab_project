from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from repository.repositories.repository_manager import RepositoryManager
from ..serializers.favor_serializer import FavorSerializer

class FavorList(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        favors = RepositoryManager().favors.get_all()
        serializer = FavorSerializer(favors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = FavorSerializer(data=request.data)
        if serializer.is_valid():
            RepositoryManager().favors.create(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavorDetail(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        return RepositoryManager().favors.get_by_id(id)

    def get(self, request, id, *args, **kwargs):
        favor = self.get_object(id)
        if favor is None:
            return Response({"detail": "Favor not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = FavorSerializer(favor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        favor = self.get_object(id)
        if favor is None:
            return Response({"detail": "Favor not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = FavorSerializer(favor, data=request.data)
        if serializer.is_valid():
            RepositoryManager().favors.update(favor, **serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        favor = self.get_object(id)
        if favor is None:
            return Response({"detail": "Favor not found."}, status=status.HTTP_404_NOT_FOUND)
        RepositoryManager().favors.delete(favor)
        return Response({"detail": "Favor was successfully deleted."}, status=status.HTTP_204_NO_CONTENT)