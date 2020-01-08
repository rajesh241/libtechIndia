"""Views Module for User App"""
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from user.serializers import UserSerializer, AuthTokenSerializer, \
                              MyTokenObtainPairSerializer, RegistrationActivationSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """View that would generate auth token"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """View that would update the user"""
    serializer_class = UserSerializer
   # authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

class MyTokenObtainPairView(TokenObtainPairView):
    """Custom token View to include custom user fields based on custom token serializer"""
    serializer_class = MyTokenObtainPairSerializer

class UserActivateView(GenericAPIView):
    """
    An Api View which provides a method to activate a user based on the token
    """
    serializer_class = RegistrationActivationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        uidb64 = serializer.validated_data['uidb64']
        token = serializer.validated_data['token']
        print(f"token-{token} uidb64-{uidb64}")
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except :
            user = None
        if not user:
            return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'status': 'OK'} )
        else:
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)


