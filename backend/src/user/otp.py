"""
Module to hold the OTP Generated Code
"""
import datetime
import requests
import pyotp
import base64

from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from core.models import OTP

User = get_user_model()

def activate_user(phone):
    """This method will active user"""
    my_user = User.objects.filter(phone=phone).first()
    if my_user is not None:
        my_user.is_active = True
        my_user.save()

class GenerateKey:
    @staticmethod
    def return_key(phone):
        return str(phone) + str(datetime.datetime.date(timezone.now())) + settings.OTP_SECRET_KEY

def send_otp(phone, otp):
    """Method to send OTP"""
    print(f"OTP for {phone} is {otp}")
    api_server = settings.SMS_API_SERVER
    username = settings.SMS_API_USERNAME
    password = settings.SMS_API_PASSWORD
    message=f"Dear User your user otp is {otp}"
    mobile_number = phone
    sender="KLPKSH"
    url = f"{api_server}/sendmessage.php?user={username}&password={password}&mobile={mobile_number}&message={message}&sender={sender}&type=3"
    res = requests.get(url)
    return res 


def verify_otp(phone, in_otp):
    """This function will regenerate the OTP and this can be used for
    verification"""
    my_otp = OTP.objects.filter(phone=phone).first()
    #In case OTP was not generated in first place
    if my_otp is None:
        return False
    #If OTP has already been used
    if my_otp.is_used == True:
        return False
    #If OTP has expired
    print(f"Current time {timezone.now()}- Expiration {my_otp.otp_expiration}")
    if timezone.now() > my_otp.otp_expiration:
        return False
    otp_counter = my_otp.otp_counter
    keygen_class = GenerateKey()
    key = base64.b32encode(keygen_class.return_key(phone).encode())
    HOTP = pyotp.HOTP(key)
    otp = HOTP.at(otp_counter)
    print(f"OTP{otp}-Verify OTP{in_otp}")
    if (str(otp) == str(in_otp).lstrip().rstrip()):
        my_otp.is_used = True  #this Flag is set so this cannot be used again
        my_otp.save()
        return True
    return False

def generate_otp(phone, for_verfication=False):
   """Method to generate OTP"""
   my_otp = OTP.objects.filter(phone=phone).first()
   if my_otp is None:
       my_otp = OTP.objects.create(phone=phone)
   otp_counter = my_otp.otp_counter + 1
   keygen_class = GenerateKey()
   key = base64.b32encode(keygen_class.return_key(phone).encode())
   HOTP = pyotp.HOTP(key)
   otp = HOTP.at(otp_counter)
   print(f"Timezone.now {timezone.now()}")
   expiration = timezone.now() + timezone.timedelta(minutes = int(settings.OTP_EXPIRATION_THRESHOLD))
   print(f"Expiration is {expiration}")
   my_otp.otp_counter = otp_counter
   my_otp.otp_expiration = expiration
   my_otp.is_used = False
   my_otp.save()
   res = send_otp(phone, otp)
   if res.status_code == 200:
       res = {'status' : 'success', 'otp' : otp}
   else:
       res = {'status' : 'fail'}
   return res
