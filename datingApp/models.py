# datingApp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    bio = models.TextField()
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    profilePicture = models.ImageField()
    password = models.CharField(max_length=200)

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set')



    def __str__(self):
        return self.username
