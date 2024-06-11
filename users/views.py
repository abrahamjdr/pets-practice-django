"""
Views for the authentication system
"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model

    This ViewSet provides CRUD operations for the User model.
    It uses the UserSerializer to serialize and deserialize User objects.

    Attributes:
        queryset (QuerySet): The queryset of all User objects.
        serializer_class (Serializer): The serializer class for User objects.

    Methods:
        list(request): Handle GET /users/ requests.
        create(request): Handle POST /users/ requests.
        retrieve(request, pk): Handle GET /users/:id requests.
        update(request, pk): Handle PUT /users/:id requests.
        partial_update(request, pk): Handle PATCH /users/:id requests.
        destroy(request, pk): Handle DELETE /users/:id requests.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        """
        Handle GET /users/ requests.

        Returns a list of all User objects.

        Args:
            request (Request): The incoming request.

        Returns:
            Response: A response containing the list of User objects.
        """
        users = self.get_queryset()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Handle POST /users/ requests.

        Creates a new User object with the provided data.

        Args:
            request (Request): The incoming request.

        Returns:
            Response: A response containing the created User object.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk):
        """
        Handle GET /users/:id requests.

        Returns a single User object by ID.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the User object.

        Returns:
            Response: A response containing the User object.
        """
        user = self.get_object()
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, pk):
        """
        Handle PUT /users/:id requests.

        Updates an existing User object with the provided data.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the User object.

        Returns:
            Response: A response containing the updated User object.
        """
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk):
        """
        Handle PATCH /users/:id requests.

        Updates an existing User object with the provided partial data.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the User object.

        Returns:
            Response: A response containing the updated User object.
        """
        user = self.get_object()
        serializer = self.serializer_class(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk):
        """
        Handle DELETE /users/:id requests.

        Deletes an existing User object by ID.

        Args:
            request (Request): The incoming request.
            pk (int): The ID of the User object.

        Returns:
            Response: A response indicating the deletion was successful.
        """
        user = self.get_object()
        user.delete()
        return Response(status=204)
