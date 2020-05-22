from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import authentication, permissions, status, generics
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
import jwt
import requests
import json
import time


class LoginAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        
        if (user is None):
            print(400)
            return JsonResponse({'status':status.HTTP_400_BAD_REQUEST,'message':'아이디 또는 패스워드가 일치하지 않습니다', 'data':None})
        
        expire_ts = int(time.time()) + 86400
        payload = {'username': username, 'expire': expire_ts}
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        token_data = token.decode('utf-8')

        expire_ts = int(time.time()) + 86400 * 14

        payload = {'username': username, 'expire': expire_ts}
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        refresh_token_data = token.decode('utf-8')
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            login(self.request, user)
        print(200)
        return JsonResponse({'status': status.HTTP_200_OK, 'message': "로그인 성공", 'data': {'login_token': token_data, 'refresh_token': refresh_token_data}})