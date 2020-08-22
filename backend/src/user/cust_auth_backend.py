"""Custom Authetication Backend"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model, authenticate
from user.otp import verify_otp
User = get_user_model()

class CustomAuthBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        username = request.data.get("username", None)
        phone = request.data.get("phone", None)
        otp = request.data.get("otp", None)
        password = kwargs['password']
        if username is not None:
            try:
                my_user = User.objects.get(username=username)
                if my_user.check_password(password) is True:
                    return my_user
            except User.DoesNotExist:
                pass
        elif phone is not None:
            try:
                my_user = User.objects.get(phone=phone)
                if otp is not None:
                    if verify_otp(phone, otp) == True:
                        return my_user
                else:
                    if my_user.check_password(password) is True:
                        return my_user
            except User.DoesNotExist:
                pass
