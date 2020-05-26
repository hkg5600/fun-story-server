from django.db import models
from django.contrib.auth.models import User
from enum import Enum

class Category(Enum):
    Fun = '100'
    Horror = '101'
    Sad= '103'
    Knowledge = '102'
    Romance = '104'
    Poem = '105'
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, to_field='username', on_delete=models.CASCADE)
    profile_image = models.FileField(blank=True,default="")

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="follower",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="user", on_delete=models.CASCADE)

class Story(models.Model):
    title = models.CharField(max_length=1000)
    description = models.CharField(max_length=100000)
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=[(category, category.value) for category in Category])
    time = models.IntegerField(default=0)
    
class Like(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
