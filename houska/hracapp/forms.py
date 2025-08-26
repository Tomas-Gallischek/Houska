from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    name = forms.CharField(label="Jméno", max_length=100, required=False)
    surname = forms.CharField(label="Příjmení", max_length=100, required=False)
    username = forms.CharField(label="Uživatelské jméno", max_length=150, required=True)
    email = forms.EmailField(label="Email", required=True)
    password1 = forms.CharField(label="Heslo", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Potvrzení hesla", widget=forms.PasswordInput, required=True)
    GENDER_CHOICES = (
        ('male', 'Muž'),
        ('female', 'Žena'),
        ('other', 'Jiné'),
    )
    gender = forms.ChoiceField(label="Pohlaví", choices=GENDER_CHOICES, required=False)
    orders = forms.IntegerField(label="Objednávky", required=False)


    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('gender', 'name', 'surname', 'email', 'orders')
