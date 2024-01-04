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
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    
class Community(models.Model):
    name = models.CharField(max_length=255)
    intro = models.CharField(max_length=500)
    members = models.ManyToManyField(User, related_name="communities")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='communities')

class Match(models.Model):
    firstUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_sent')
    secondUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_received')
    matched_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

class Chat(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='chats')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_chats")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
