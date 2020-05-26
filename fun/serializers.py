from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category,
    Follow,
    Like,
    Story,
    UserProfile,
    Save,
)

class StorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Story
        fields = ('id','title','description','user', 'category')

class StoryCountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Story
        fields = '__all__'

class UserSerialzier(serializers.ModelSerializer):
    profile_image = serializers.FileField(source='userprofile.profile_image', read_only=True)
    class Meta:
        model = User
        fields = ('id','username','profile_image')
   