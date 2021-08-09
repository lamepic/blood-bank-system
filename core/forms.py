from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

from accounts.models import UserProfile
from .models import (
    Appointment, 
    BloodDonation, 
    Stock,
    Hospital,
    Withdraw,
)

User = get_user_model()

class AppForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['donate_date']


class UserProfileEditForm(forms.ModelForm):
    age = forms.IntegerField()

    class Meta:
        model = UserProfile
        fields = ['age', 'address', 'phone', 'gender', 'blood_group']

    def clean_age(self, *args, **kwargs):
        age = self.cleaned_data['age']

        if age < 18:
            raise forms.ValidationError("Your age cannot be less than 18")

        return age

class UserEditForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class BloodDonationForm(forms.ModelForm):
    class Meta:
        model = BloodDonation
        fields = ['blood_volume', 'blood_type']

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['blood_type', 'blood_volume', 'expire_date']

# class WithdrawForm(forms.ModelForm):
#     class Meta:
#         model = Withdraw
#         fields = ['blood_type', 'withdraw_date']