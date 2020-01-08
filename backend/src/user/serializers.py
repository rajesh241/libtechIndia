"""
Serializer Module for User
"""
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        """Default Meta Class"""
        model = get_user_model()
        fields = ('email', 'password', 'password2', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def validate(self, data):
        print(f"data is {data}")
        pass1 = data.get('password')
        pass2 = data.pop('password2', None)
        if pass1 != pass2:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        """Create function of serializer"""
        my_user = get_user_model().objects.create_user(**validated_data)
        request=self.context.get('request'),
        self.send_account_activation_email(request, my_user)
        return my_user

    def update(self, instance, validated_data):
        """Update function of serializer"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def send_account_activation_email(self, request, user):
        text_content = 'Account Activation Email'
        subject = 'Email Activation'
        template_name = "activation.html"
        from_email = settings.EMAIL_HOST_USER
        recipients = [user.email]
        kwargs = {
            "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user)
        }
        print(str(kwargs))
        activate_url = str(kwargs)
        context = {
            'user': user,
            'activate_url': activate_url
        }
        html_content = render_to_string(template_name, context)
        email = EmailMultiAlternatives(subject, text_content, from_email, recipients)
        email.attach_alternative(html_content, "text/html")
        email.send()
 

class AuthTokenSerializer(serializers.Serializer):
    """Serializer class for issuing auth Token"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validating the submitted username and password"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate user with provied credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custome token serializer to include custom user fields in the token"""
    @classmethod
    def get_token(cls, user):
        """Overriding get token method"""
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['name'] = user.email
        return token


class RegistrationActivationSerializer(serializers.Serializer):
    token = serializers.CharField()
    uidb64 = serializers.CharField()
