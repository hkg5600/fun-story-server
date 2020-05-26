# -*- coding: utf-8 -*-
import requests, jwt, time
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
from django.contrib.auth.backends import BaseBackend
User = get_user_model()

class MyBackend(BaseBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

class MyTokenAuthentication():
    authentication_header_prefix ='Token'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()
        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')
        
        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            return None
        expire = payload.get('expire')
        if int(time.time()) > expire:
            return None
        user_id = payload.get('username')
        try:
            user = User.objects.get(username=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user1'+str(payload)+str(user_id))
        return (user, token)

    def authenticate_header(self, request):
        return self.authentication_header_prefix
