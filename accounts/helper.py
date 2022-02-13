from kavenegar import * # A webservice for phone verification
from random import randint # Random number for phone verification 
from zeep import Client # zeep is advanced library to handle SOAP communications in python.
from .models import User
import datetime



def send_otp(mobile_phone, otp):
    mobile_phone = ['mobile_phone',]
    try:
        api = KavenegarAPI('70536C72346671366C5272546E31736D77526430654157684935526B516237376232444B6C6B716169636B3D')
        params = {
            'sender': '10008663',#optional
            'receptor': mobile_phone,#multiple mobile number, split by comma
            'message': f'The code is {otp}',
        } 
        response = api.sms_send(params)
        print('OTP: ', otp)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)

def send_otp_soap(mobile_phone, otp):
    client = Client('http://api.kavenegar.com/soap/v1.asmx?WSDL')
    receptor = ['mobile_phone',]

    empty_array_placeholder = client.get_type('ns0:ArrayOfString')
    receptors = empty_array_placeholder()
    for item in receptor:
        receptors['string'].append(item)

    api_key = '70536C72346671366C5272546E31736D77526430654157684935526B516237376232444B6C6B716169636B3D'
    message = f'The code is {otp}'
    sender = '10008663'
    status = 0
    status_message = ''

    result = client.service.SendSimpleByApikey(api_key, sender, message, receptors, 0, 1, status, status_message)
    print(result)
    print(f'OTP: {otp}')

def get_random_otp():
    return randint(1000, 9999)

def check_otp_expiration(mobile_phone):
    try:
        user = User.objects.get(mobile_phone=mobile_phone)
        now = datetime.datetime.now()
        otp_time = user.otp_created
        diff_time = now - otp_time
        print('OTP TIME: ', diff_time)

        if diff_time.seconds > 120:
            return False
        return True

    except User.DoesNotExist:
        return False