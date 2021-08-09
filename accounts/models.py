from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
GENEDR = (
        ('F', 'Female'),
        ('M', 'Male'),
)

BLOOD_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
)


class User(AbstractUser):
    is_normalUser = models.BooleanField(default=False)
    is_staffUser = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1, choices=GENEDR)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=3, choices=BLOOD_CHOICES)

    def __str__(self):
        return self.user.username

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username
    