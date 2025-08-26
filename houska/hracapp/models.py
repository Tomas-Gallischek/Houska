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
    gold = models.IntegerField(("Počet GOLDŮ"), default=1)
    rohlik = models.IntegerField(("Počet ROHLÍKŮ"), default=1)
    gold_grow = models.IntegerField(("Růst GOLDŮ za 1s"), default=1)
    last_gold_collection = models.DateTimeField(blank=True, null=True, default=models.functions.Now)

    def __str__(self):
        return self.username

