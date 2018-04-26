from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from builtins import *
import hashlib
import time
from django.conf import settings


def cal_token(*args):
    s = ''.join(sorted([str(a) for a in args]))
    sha1 = hashlib.sha1()
    sha1.update(s.encode('utf-8'))
    key = sha1.hexdigest()
    return key


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if request.method == 'GET':
            return

        # if settings.DEBUG:
        #     return
        print(request.data)
        print('++++++', request.META)
        username = request.META.get('HTTP_X_USERNAME')
        token = request.META.get('HTTP_X_TOKEN')
        unix_time = request.META.get('HTTP_X_UNIX_TIME', 0)

        if not username and not token and not unix_time:
            try:
                username = request.data.get('x_username')
                token = request.data.get('x_token')
                unix_time = request.data.get('x_unit_time')
            except:
                raise exceptions.AuthenticationFailed('Token Auth Failed')

        print(username, token, unix_time)
        if abs(float(unix_time) - time.time()) > 60:
            raise exceptions.AuthenticationFailed('Token Auth Failed')

        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Token Auth Failed')

        try:
            private_key=Token.objects.get(user=user).key
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('Token Auth Failed')

        check_token=cal_token(username, unix_time, private_key)

        if check_token != token:
            raise exceptions.AuthenticationFailed('Token Auth Failed')

        return (user, None)
