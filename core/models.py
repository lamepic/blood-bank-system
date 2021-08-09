from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.
User = get_user_model()

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

STATUS = (
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('F', 'Failed')
)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    donate_date = models.DateField('Appointment Date', help_text="YYYY-MM-DD")
    status = models.CharField(max_length=1, choices=STATUS, default='P')

    def __str__(self):
        return self.user.username
    

class Stock(models.Model):
    blood_type = models.CharField(max_length=3, choices=BLOOD_CHOICES)
    blood_volume = models.IntegerField(default=0)
    receive_date = models.DateField(auto_now_add=True)
    expire_date = models.DateField()
    expire_status = models.BooleanField(default=False)

    def __str__(self):
        return self.blood_type
    

class BloodDonation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blooddonations')
    # appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='blooddonations')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='blooddonations')
    blood_volume = models.IntegerField(default=0)
    donate_date = models.DateField(auto_now_add=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_CHOICES)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-donate_date']
    


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:hospital_detail", kwargs={"id": self.id})
    
    

class BloodRequest(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='bloodrequests')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='bloodreuqests')
    blood_type = models.CharField(max_length=3, choices=BLOOD_CHOICES)
    withdraw_date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    request_amount = models.IntegerField(default=1)

    def __str__(self):
        return self.blood_type

    class Meta:
        ordering = ['-withdraw_date']
    

class Withdraw(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='withdraws')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='withdraws')
    blood_request = models.ForeignKey(BloodRequest, on_delete=models.CASCADE, related_name='withdraws')
    blood_type = models.CharField(max_length=3, choices=BLOOD_CHOICES)
    withdraw_date = models.DateField()

    def __str__(self):
        return self.hospital.name

    class Meta:
        ordering = ['-withdraw_date']
    
