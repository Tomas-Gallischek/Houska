from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    GENDER_CHOICES = (
        ('male', 'Muž'),
        ('female', 'Žena'),
        ('other', 'Jiné'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    orders = models.IntegerField(("Počet objednávek"), blank=True, null=True)
    def __str__(self):
        return self.username

#POKUD ZDE PŘIDÁŠ NOVÝ MODEL, JE TŘEBA JEJ PŘIDAT I D OREGISTRAČNÍHO FORMULÁŘE