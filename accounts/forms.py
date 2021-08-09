from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import UserProfile, StaffProfile

User = get_user_model()

class UserForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class UserEditForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserProfileForm(forms.ModelForm):
    age = forms.IntegerField()

    class Meta:
        model = UserProfile
        fields = ['gender', 'age', 'address', 'blood_group', 'phone']

    def clean_age(self, *args, **kwargs):
        age = self.cleaned_data['age']

        if age < 18:
            raise forms.ValidationError("You should be 18 or Older to donate blood")

        return age

class UserProfileEditForm(forms.ModelForm):
    age = forms.IntegerField()

    class Meta:
        model = UserProfile
        fields = ['age', 'address', 'phone']

    def clean_age(self, *args, **kwargs):
        age = self.cleaned_data['age']

        if age < 18:
            raise forms.ValidationError("Your age cannot be less than 18")

        return age


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Wrong Username or password")
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
            if not user.is_active:
                raise forms.ValidationError("User is not Active")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class StaffProfileForm(forms.ModelForm):

    class Meta:
        model = StaffProfile
        exclude = ['user']

