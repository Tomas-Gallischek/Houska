from django.shortcuts import render, redirect
from . import rasy_povolani
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Playerinfo



@login_required
def atributy_hodnota(request):
    user = request.user
    rasy_povolani.rasa_bonus(request)

    # Výpočet HP
    hp_bonus_procenta = round(user.vitality/10, 2)
    if hp_bonus_procenta <= 1:
        hp_bonus_procenta = 1
    hp = round(((((user.lvl) + (user.lvl*3))) * user.hp_bonus)*(hp_bonus_procenta)) # <-- 10 vit = +1%

    user.hp = hp

    # Vypsání atributů z databáze + BASE staty
    charisma = user.charisma + user.charisma_base
    dexterity = user.dexterity + user.dexterity_base
    intelligence = user.intelligence + user.intelligence_base
    luck = user.luck + user.luck_base
    strength = user.strength + user.strength_base
    vitality = user.vitality + user.vitality_base

    atributy = {
        'HP': int(hp),
        'charisma': int(charisma),
        'dexterity': int(dexterity),
        'intelligence': int(intelligence),
        'luck': int(luck),
        'strength': int(strength),
        'vitality': int(vitality),
        'hp_bonus_procenta': int(hp_bonus_procenta)
    }


    user.save()
    return atributy

def atributy_cena(request):

    user = atributy_hodnota(request)
    hp = user['HP']
    charisma = user['charisma']
    dexterity = user['dexterity']
    intelligence = user['intelligence']
    luck = user['luck']
    strength = user['strength']
    vitality = user['vitality']

    charisma_price = (charisma - request.user.charisma_base) + ((charisma - request.user.charisma_base) * 1.5)
    dexterity_price = (dexterity - request.user.dexterity_base) + ((dexterity - request.user.dexterity_base) * 1.5)
    intelligence_price = (intelligence - request.user.intelligence_base) + ((intelligence - request.user.intelligence_base) * 1.5)
    luck_price = (luck - request.user.luck_base) + ((luck - request.user.luck_base) * 1.5)
    strength_price = (strength - request.user.strength_base) + ((strength - request.user.strength_base) * 1.5)
    vitality_price = (vitality - request.user.vitality_base) + ((vitality - request.user.vitality_base) * 1.5)

    cena = {
        'charisma_price': int(charisma_price),
        'dexterity_price': int(dexterity_price),
        'intelligence_price': int(intelligence_price),
        'luck_price': int(luck_price),
        'strength_price': int(strength_price),
        'vitality_price': int(vitality_price)
    }

    return cena

def calculate_xp_and_level(request):
    user = request.user
    steps = user.steps if user.steps is not None else 0
    XP_aktual = steps
    lvl_aktual = 1
    lvl_next = 2
    XP_potrebne_next = round((22*lvl_aktual)*((lvl_next)*1.1))

    for lvl in range(1, 500):
        XP_potrebne = round((22*lvl)*((lvl**1.1)))
        if XP_aktual >= XP_potrebne:
            XP_aktual -= XP_potrebne
            lvl_aktual += 1
            lvl_next = lvl_aktual + 1
            XP_potrebne_next = round((22*lvl_next)*((lvl_next**1.1)))
        else:
            user.xp = XP_aktual
            user.lvl = lvl_aktual
            user.save()
            break

    return XP_aktual, lvl_aktual, lvl_next, XP_potrebne_next


def calculate_gold(user, lvl_aktual):
    # Koeficient růstu goldů
    if user.gold_growth_coefficient is not None:
        if lvl_aktual == 1:
            gold_growth_coefficient = 0.1
        else:
            gold_growth_coefficient = (lvl_aktual / 10)
        user.gold_growth_coefficient = gold_growth_coefficient
        user.save()
    else:
        gold_growth_coefficient = 0.1

    # VÝPOČET NASBÍRANÝCH GOLDŮ
    time_since_last_collection = timezone.now() - user.last_gold_collection
    seconds_since_last_collection = time_since_last_collection.total_seconds()

    collected_gold = min(int(seconds_since_last_collection), 28800) * gold_growth_coefficient
    gold_per_hour = round(gold_growth_coefficient * 3600)
    gold_limit = gold_per_hour * 8  # Limit pro zobrazení

    user.save()
    return round(collected_gold,2), round(gold_growth_coefficient,2), round(gold_limit,2), round(gold_per_hour,2)




