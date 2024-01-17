"""
URL configuration for friendApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import UserList, UserDetailAPI, RegisterUserAPIView, LoginView, CategoryList, CommunityList, join_community, UsersInCommunityView, MatchListCreateView, MatchAcceptView

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('users/', UserList.as_view(), name = 'user-list'),
    path('user-details/<int:user_id>', UserDetailAPI.as_view(), name='user_detail'),
    path('register', RegisterUserAPIView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('categories/', CategoryList.as_view()),
    path('community/', CommunityList.as_view()),
    path('join-community/', join_community, name='join-community'),
    path('community/<int:community_id>/users/', UsersInCommunityView.as_view()),
    path('matches/', MatchListCreateView.as_view()),
    path('match/<int:pk>/accept/', MatchAcceptView.as_view())
]
