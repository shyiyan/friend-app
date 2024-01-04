# datingApp/views.py
from rest_framework import generics
from .models import User, Category
from .serializers import UserSerializer, RegisterSerializer, UserLoginSerializer, CategorySerializer

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
#from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model 




from rest_framework.authtoken.models import Token

from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

from django.shortcuts import get_object_or_404




class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )
    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=email)


        if user.check_password(password):

            token, created = Token.objects.get_or_create(user=user)
            response_data = {
                'token': token.key,
                'user' : UserLoginSerializer(user).data
             }
            return Response(response_data)
        else:
           return Response({'error': 'Invalid credentials'}, status=401)
        
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
