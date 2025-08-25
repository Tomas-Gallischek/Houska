from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Uživatelské jméno", max_length=150, required=True)
    email = forms.EmailField(label="Email", required=True)
    password1 = forms.CharField(label="Heslo", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Potvrzení hesla", widget=forms.PasswordInput, required=True)

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('gender',)