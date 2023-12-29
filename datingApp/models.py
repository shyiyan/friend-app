# datingApp/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    bio = models.TextField()
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    profilePicture = models.ImageField()
    password = models.CharField(max_length=200)


    def __str__(self):
        return self.username
