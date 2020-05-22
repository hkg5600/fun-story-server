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
