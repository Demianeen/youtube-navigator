from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser

# Create your models here.

class MyUser(AbstractUser):
    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(max_length = 200, unique = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']