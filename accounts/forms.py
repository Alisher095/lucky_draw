# accounts/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import Profile, Draw


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            raise forms.ValidationError("Passwords do not match")
        return cleaned


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', max_length=30, required=True)
    last_name  = forms.CharField(label='Last Name',  max_length=30, required=True)
    email      = forms.EmailField(label='Email',     required=True)

    class Meta:
        model = Profile
        fields = ['role']
        widgets = {
            'role': forms.TextInput(
                attrs={'readonly': 'readonly', 'class': 'form-control-plaintext'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial  = self.instance.user.last_name
            self.fields['email'].initial      = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        user.email      = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile


class DrawForm(forms.ModelForm):
    class Meta:
        model = Draw
        fields = [
            'title',
            'draw_type',
            'description',
            'prize_name',
            'prize_value',
            'winners_count',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter draw title'
            }),
            'draw_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the draw, prizes, and instructions'
            }),
            'prize_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prize name (e.g., Amazon Gift Card)'
            }),
            'prize_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Prize value (e.g., 50.00)'
            }),
            'winners_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'How many winners?'
            }),
        }
