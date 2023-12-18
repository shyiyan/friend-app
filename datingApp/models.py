# datingApp/models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    bio = models.TextField()
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    email = models.EmailField()
    profilePicture = models.ImageField()

    def __str__(self):
        return self.username
