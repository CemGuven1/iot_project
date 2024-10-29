from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Device, Project  # Assuming you have a Project model
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        email = forms.EmailField(required=True, label='Email')
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
        }


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_id', 'name']  # Add any other necessary fields
        widgets = {
            'device_id': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),  # Ensure type is text
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_device_id(self):
        device_id = self.cleaned_data['device_id']
        if not device_id.isdigit():  # Check if the device_id consists of only digits
            raise ValidationError("Device ID must be numeric.")
        return device_id
    
    
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']  # Add any other fields you need
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
