from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('verify/', views.VerifyToken.as_view()),
    path('refresh/', views.RefreshToken.as_view()),
    path('login/', views.LoginAPI.as_view()),
    path('join/', views.JoinAPI.as_view()),
    path('my-story/',views.GetSavedStoryAPI.as_view()),
    path('write-story/', views.WriteStoryAPI.as_view()),
    path('save-story/<int:story>/', views.SaveStoryAPI.as_view()),
    path('save-story/', views.SaveStoryAPI.as_view()),
    path('story/<int:page>/<int:user>/<int:follow>/<int:category>/', views.GetStoryAPI.as_view()),
    path('story/<int:page>/<int:user>/<int:follow>/', views.GetStoryAPI.as_view()),
    path('story/<int:page>/<int:user>/', views.GetStoryAPI.as_view()),
    path('story/<int:id>/', views.GetStoryAPI.as_view()),
    path('follow/<int:user>/', views.FollowUserAPI.as_view()),
    path('my-follow/<int:page>/', views.GetFollowerAPI.as_view()),
    path('story-detail/<int:id>/', views.GetStoryDetailAPI.as_view()),
    path('profile/', views.UserProfileAPI.as_view()),
    path('user/<int:id>/', views.UserInfoAPI.as_view()),
    path('user-info/<int:id>/', views.UserInfoWithFollowAPI.as_view()),
    path('my-info/', views.MyInfoAPI.as_view()),
]