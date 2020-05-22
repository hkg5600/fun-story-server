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
from .serializers import (
    StorySerializer,
    UserSerialzier,
    StoryCountSerializer,
)

from .models import (
    Category,
    Follow,
    Like,
    Story,
    UserProfile,
    Save,
)

class UserInfoAPI(APIView):
    def get(self, request, id=None, format=None):
        user = User.objects.get(id=id)
        serializer = UserSerialzier(user, many=False)
        return JsonResponse({'status': status.HTTP_200_OK, 'message': "success to find", 'data': serializer.data})
class UserProfileAPI(APIView):
    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = (self.get_object()).userprofile
        user.profile_image = request.data.get('image')
        user.save()
        return JsonResponse({'status': status.HTTP_200_OK, 'message': "success to save", 'data': ''})

class GetFollowerAPI(APIView): # Done
    def get_object(self):
        return self.request.user

    def get(self, request, page=None, format=None):
        user = self.get_object()
        follower_id_list = Follow.objects.filter(user=user).values_list('follower', flat=True)[page*10:(page+1)*10]
        query = User.objects.filter(id__in=follower_id_list)
        is_last_page = False
        next_page = page + 1
        if (query.count() < 10):
            is_last_page = True
            next_page = -1
        serializer = UserSerialzier(query, many=True)
        
        return JsonResponse({'status': status.HTTP_200_OK, 'message': "story list", 'data': {'follower_list':serializer.data, 'last_page':is_last_page, 'next_page':next_page}})

class FollowUserAPI(APIView): # Done
    def get_object(self):
        return self.request.user

    def get(self, request, user=None, format=None):
        me = self.get_object()
        follow = Follow.objects.create(user=me, follower=User.objects.get(id=user))
        follow.save()
        
        return JsonResponse({'status': status.HTTP_200_OK, 'message': "success to follow", 'data': ''})

class SaveStoryAPI(APIView): # Done

    def get_object(self):
        return self.request.user

    def get(self, request, story=None, format=None):
        user = self.get_object()
        story = Save.objects.create(user=user, story=Story.objects.get(id=story))
        story.save()
        
        return JsonResponse({'status': status.HTTP_200_OK, 'message': "success to save", 'data': ''})


class GetSavedStoryAPI(APIView): # Done

    def get_object(self):
        return self.request.user

    def get(self, request, page=None,format=None):
        user = self.get_object()
        story_id_list = Save.objects.filter(user=user).values_list('story', flat=True)[page*10:(page+1)*10]
        query = Story.objects.filter(id__in=story_id_list)
        is_last_page = False
        next_page = page + 1
        if (query.count() < 10):
            is_last_page = True
            next_page = -1
        serializer = StorySerializer(query, many=True)
        
        return JsonResponse({'status': status.HTTP_200_OK, 'message': "story list", 'data': {'story_list':serializer.data, 'last_page':is_last_page, 'next_page':next_page}})

class GetStoryAPI(APIView): # Done
    permission_classes = (AllowAny,)
    
    def get_object(self):
        return self.request.user

    def get(self, request, page=None,user=None, follow=None, category=None,format=None):
        if (user is not None and user is not 0):
            owner = User.objects.get(id=user)
            query = Story.objects.filter(user=owner)[page*10:(page+1)*10]
        else:
            if (follow is not False):
                follow = Follow.objects.filter(user=self.get_object()).values_list('follower', flat=True)
                print(follow)
                if (category is not None):
                    query = Story.objects.filter(user__in=follow, category=category)[page*10:(page+1)*10]
                else:
                    query = Story.objects.filter(user__in=follow)[page*10:(page+1)*10]
            else:
                if (category is not None):
                    query = Story.objects.filter(category=category)[page*10:(page+1)*10]
                else:
                    query = Story.objects.all()[page*10:(page+1)*10]    
                
        is_last_page = False
        next_page = page + 1
        if (query.count() < 10):
            is_last_page = True
            next_page = -1
        serializer = StorySerializer(query, many=True)
        return JsonResponse({'status': status.HTTP_200_OK, 'message': "story list", 'data': {'story_list':serializer.data, 'last_page':is_last_page, 'next_page':next_page}})

class GetStoryDetailAPI(APIView):

    def get_object(self):
        return self.request.user


    def get(self, request, id=None, *args, **kwargs):

        story = Story.objects.get(id=id)
        story.time = story.time + 1
        story.save()
        serializer = StoryCountSerializer(story, many=False)
        
        return JsonResponse({'status': status.HTTP_200_OK, 'message': "story list", 'data': serializer.data})


class WriteStoryAPI(APIView): # Done

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        title = request.data.get("title")
        description = request.data.get("description")
        category = request.data.get("category")
        if (user is None or title is None or description is None):
              return JsonResponse({'status': status.HTTP_404_NOT_FOUND, 'message': "data is not satisfied", 'data': ''})
            
        story = Story.objects.create(user=user, title=title, description=description, category=category)
        story.save()

        return JsonResponse({'status': status.HTTP_200_OK, 'message': "success to write", 'data': ''})


class JoinAPI(APIView): # Done
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')
        if (username is None or password1 is None or password2 is None):
            return JsonResponse({'status': status.HTTP_404_NOT_FOUND, 'message': "데이터가 요구조건을 만족하지 못합니다", 'data': ''})

        if (password1 != password2):
            return JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'message': "비밀번호가 일치하지 않습니다", 'data': ''})

        user = User.objects.filter(username=username)

        if (user.exists()):
            return JsonResponse({'status': status.HTTP_403_FORBIDDEN, 'message': "이미 존재하는 아이디입니다", 'data': ''})
        
        user = User.objects.create_user(username=username, password=password1)
        UserProfile.objects.create(user=user)
        return JsonResponse({'status': status.HTTP_200_OK, 'data': "", 'message': "회원가입 성공"})

class LoginAPI(APIView): # Done
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