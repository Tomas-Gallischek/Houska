from django.db import models
from django.contrib.auth.models import AbstractUser

class Playerinfo(AbstractUser):

    GENDER_CHOICES = (
        ('male', 'Muž'),
        ('female', 'Žena'),
        ('other', 'Jiné'),
    )

    FRAKCE_CHOICES = (
        ('Light Side', 'Světlo'),
        ('Dark Side', 'Prázdnota'),
    )

    if FRAKCE_CHOICES == 'Light Side':
        RASA_CHOICES = (
            ('human', 'Člověk'),
            ('elf', 'Elf'),
            ('dwarf', 'Trpaslík'),
        )
    elif FRAKCE_CHOICES == 'Dark Side':
        RASA_CHOICES = (
            ('Urgal', 'Urgal'),
            ('Gnóm', 'Gnóm'),
            ('Dark Elf', 'Temný Elf'),
        )
    else:
        RASA_CHOICES = None

    if FRAKCE_CHOICES == 'Light Side':
        POVOLANI_CHOICES = (
            ('HUNTER', 'Bojovník'),
            ('PRIEST', 'Kněz'),
            ('WARRIOR', 'Válečník'),
            ('PALADIN', 'Paladin'),
            ('MAGE', 'Mág')
        )
    elif FRAKCE_CHOICES == 'Dark Side':
        POVOLANI_CHOICES = (
            ('ROGUE', 'Roguna'),
            ('NECROMANCER', 'Nekromant'),
            ('BERSERKER', 'Berserk'),
            ('WARLOCK', 'Temný mág'),
            ('DRUID', 'Druid')
        )
    else:
        POVOLANI_CHOICES = None

    # OSOBNÍ INFORMACE O HRÁČI
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    steps = models.IntegerField(("Počet kroků"), blank=True, null=True)

    # ZÁKLADNÍ INFORMACE O HRÁČOVĚ POSTAVĚ
    lvl = models.IntegerField(("Úroveň"), default=1, blank=True, null=True)
    xp = models.IntegerField(("Zkušenosti"), default=0, blank=True, null=True)
    frakce = models.CharField(max_length=20, choices=FRAKCE_CHOICES, blank=True, null=True)
    rasa = models.CharField(max_length=20, choices=RASA_CHOICES, blank=True, null=True)
    povolani = models.CharField(max_length=20, choices=POVOLANI_CHOICES, blank=True, null=True)

    # EKONOMICKÉ INFORMACE O HRÁČI
    gold = models.IntegerField(("Počet GOLDŮ"), default=1)
    rohlik = models.IntegerField(("Počet ROHLÍKŮ"), default=1)
    gold_growth_coefficient = models.FloatField(("Koeficient růstu GOLDŮ"), default=1.0)
    last_gold_collection = models.DateTimeField(blank=True, null=True, default=models.functions.Now)

    # ATRIBUTY HRÁČOVY POSTAVY
    HP = models.IntegerField(("Počet životů"), default=10, blank=True, null=True)
    strength = models.IntegerField(("Síla"), default=1, blank=True, null=True)
    dexterity = models.IntegerField(("Obratnost"), default=1, blank=True, null=True)
    intelligence = models.IntegerField(("Inteligence"), default=1, blank=True, null=True)
    charisma = models.IntegerField(("Charisma"), default=1, blank=True, null=True)
    vitality = models.IntegerField(("Vitalita"), default=1, blank=True, null=True)
    skill = models.IntegerField(("Zručnost"), default=1, blank=True, null=True)


    def __str__(self):
        return self.username

