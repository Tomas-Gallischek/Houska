from django.db import models
from django.contrib.auth.models import AbstractUser

class Playerinfo(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    GENDER_CHOICES = (
        ('male', 'Muž'),
        ('female', 'Žena'),
        ('other', 'Jiné'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    steps = models.IntegerField(("Počet kroků"), blank=True, null=True)
    gold = models.IntegerField(("Počet GOLDŮ"), default=1)
    rohlik = models.IntegerField(("Počet ROHLÍKŮ"), default=1)
    gold_growth_coefficient = models.FloatField(("Koeficient růstu GOLDŮ"), default=1.0)
    last_gold_collection = models.DateTimeField(blank=True, null=True, default=models.functions.Now)
    HP = models.IntegerField(("Počet životů"), default=10, blank=True, null=True)
    strength = models.IntegerField(("Síla"), default=1, blank=True, null=True)
    dexterity = models.IntegerField(("Obratnost"), default=1, blank=True, null=True)
    intelligence = models.IntegerField(("Inteligence"), default=1, blank=True, null=True)
    charisma = models.IntegerField(("Charisma"), default=1, blank=True, null=True)
    vitality = models.IntegerField(("Vitalita"), default=1, blank=True, null=True)
    skill = models.IntegerField(("Zručnost"), default=1, blank=True, null=True)


    def __str__(self):
        return self.username

