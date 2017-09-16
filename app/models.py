
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from datetime import datetime

# extend the AbstractBaseUser class to use the Django user user function
class User(AbstractBaseUser):

    username = models.CharField(max_length=255, unique = True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'
    objects = UserManager()

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(default="")
    category = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(default=datetime.now)
   

class Comment(models.Model):

    body = models.TextField(default="")
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(default=datetime.now)