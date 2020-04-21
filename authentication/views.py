from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, TokenSerializer)


def create_auth_token(user):
    """
    Returns the token required for authentication for a user.
    """
    token, _ = Token.objects.get_or_create(user=user)
    return token


class LoginView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Takes the username and password as input, validates them\
        and returns the **REST Token** (Authentication Token),\
        if the credentials are valid.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = create_auth_token(user)
        response = TokenSerializer({'token': token})
        return Response(response.data, status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        Registers a users in Django by taking the name, email,\
        username and password as input. Username and password\
        are required for login.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = create_auth_token(user)
        response = TokenSerializer({'token': token})
        return Response(response.data, status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    """
    Retrieves the id, name, email and username of the logged in user.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user