# datingApp/views.py
from rest_framework import generics
from .models import User, Category, Community, Match
from .serializers import UserSerializer, RegisterSerializer, UserLoginSerializer, CategorySerializer, CommunitySerializer, JoinCommunitySerializer, MatchSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated
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

from rest_framework.decorators import api_view, permission_classes




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

class CommunityList(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    
#when testing in postman, add header with key "Authorization",  value "Token your_token"
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_community(request):
    serializer = JoinCommunitySerializer(data=request.data)

    if serializer.is_valid():
        community_id = serializer.validated_data['community_id']
        try:
            community = Community.objects.get(pk=community_id)
            community.members.add(request.user)
            return Response({'message': 'Joined community successfully'}, status=200)
        except Community.DoesNotExist:
            return Response({'error': 'Community not found'}, status=404)
    else:
        print(serializer.errors)
        return Response({'error': 'Invalid data.'}, status=400)
    


class UsersInCommunityView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        community_id = self.kwargs.get('community_id')
        community = Community.objects.get(pk=community_id)
        return community.members.all()
    
class MatchListCreateView(generics.ListCreateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

class MatchAcceptView(generics.RetrieveUpdateAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.accepted = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)