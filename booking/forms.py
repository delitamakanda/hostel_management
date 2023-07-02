from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from booking.models import Guest



class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': 'Enter your username same as your roll no.',
        }

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    class Meta:
        model = Guest
        fields = [
            'guest_name',
            'guest_email',
            'guest_phone',
            'enrollment_no',
            'book',
            'date_of_birth',
            'gender',
        ]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            'room'
        ]