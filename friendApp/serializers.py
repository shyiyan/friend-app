# datingApp/serializers.py
from rest_framework import serializers
from .models import User, Category, Community, Match
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'bio', 'firstName', 'lastName', 'email', 'profilePicture')

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
                                   )
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email', 'password')
        
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
                                   )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'firstName', 'lastName')
        extra_kwargs = {
            'firstName' : {'required': True},
            'lastName' : {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password incorrect"}
            )
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            password = validated_data['password']
        )
    
        user.set_password(validated_data['password'])
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True, 
        validators=[UniqueValidator(queryset=Category.objects.all())]
                                   )
    class Meta:
        model = Category
        fields = ['name']

class CommunitySerializer(serializers.ModelSerializer):
    member = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Community
        fields = ('name', 'intro', 'member', 'category')


class JoinCommunitySerializer(serializers.Serializer):
    community_id = serializers.IntegerField()

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'