from django.db import models
from django.contrib.auth.models import AbstractUser

class Playerinfo(AbstractUser):

    GENDER_CHOICES = (
        ('male', 'Muž'),
        ('female', 'Žena'),
        ('other', 'Jiné'),
    )

    RASA_CHOICES = (
            ('Choice:', 'Vyber:'),
            ('human', 'Člověk'),
            ('elf', 'Elf'),
            ('dwarf', 'Trpaslík'),
            ('urgal', 'Urgal'),
            ('gnóm', 'Gnóm'),
            ('shadow', 'Stín'),
        )

    POVOLANI_CHOICES = (
            ('choice:', 'Vyber:'),
            ('ranger', 'Hraničář'),
            ('monk', 'Mnich'),
            ('warrior', 'Válečník'),
            ('paladin', 'Paladin'),
            ('mage', 'Mág'),
            ('rogue', 'Roguna'),
            ('necromancer', 'Nekromant'),
            ('berserker', 'Ničitel'),
            ('druid', 'Druid')
        )

    # OSOBNÍ INFORMACE O HRÁČI
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    steps = models.IntegerField(("Počet kroků"), blank=True, null=True)

    # ZÁKLADNÍ INFORMACE O HRÁČOVĚ POSTAVĚ
    lvl = models.IntegerField(("Úroveň"), default=1, blank=True, null=True)
    xp = models.IntegerField(("Zkušenosti"), default=0, blank=True, null=True)
    rasa = models.CharField(max_length=20, choices=RASA_CHOICES, blank=True, null=True)
    povolani = models.CharField(max_length=20, choices=POVOLANI_CHOICES, blank=True, null=True)

    # EKONOMICKÉ INFORMACE O HRÁČI
    gold = models.IntegerField(("Počet GOLDŮ"), default=1)
    rohlik = models.IntegerField(("Počet ROHLÍKŮ"), default=1)
    gold_growth_coefficient = models.FloatField(("Koeficient růstu GOLDŮ"), default=1.0)
    last_gold_collection = models.DateTimeField(blank=True, null=True, default=models.functions.Now)

    # ATRIBUTY HRÁČOVY POSTAVY
    HP = models.IntegerField(("Počet životů"), default=10, blank=True, null=True)
    hp_bonus = models.FloatField(("Bonus k životům"), default=1, blank=True, null=True)
    strength = models.IntegerField(("Síla"), default=1, blank=True, null=True)
    strength_base = models.IntegerField(("Základní síla"), default=1, blank=True, null=True)
    dexterity = models.IntegerField(("Obratnost"), default=1, blank=True, null=True)
    dexterity_base = models.IntegerField(("Základní obratnost"), default=1, blank=True, null=True)
    intelligence = models.IntegerField(("Inteligence"), default=1, blank=True, null=True)
    intelligence_base = models.IntegerField(("Základní inteligence"), default=1, blank=True, null=True)
    charisma = models.IntegerField(("Charisma"), default=1, blank=True, null=True)
    charisma_base = models.IntegerField(("Základní charisma"), default=1, blank=True, null=True)
    vitality = models.IntegerField(("Vitalita"), default=1, blank=True, null=True)
    vitality_base = models.IntegerField(("Základní vitalita"), default=1, blank=True, null=True)
    luck = models.IntegerField(("Zručnost"), default=1, blank=True, null=True)
    luck_base = models.IntegerField(("Základní zručnost"), default=1, blank=True, null=True)

    dmg_atribut = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

