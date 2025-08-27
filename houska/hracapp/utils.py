from django.shortcuts import render, redirect

from . import rasy_povolani
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Playerinfo




def atributy_funkce(request):
    user = request.user
    rasa = rasy_povolani.rasa_bonus(request)
    rasa_bonus_hp = rasa['hp_bonus']
    # Výpočet HP
    hp = (user.lvl) + (user.lvl*5) + (user.lvl**2) + rasa_bonus_hp
    user.hp = hp

    # Vypsání atributů z databáze
    charisma = user.charisma
    dexterity = user.dexterity
    intelligence = user.intelligence
    skill = user.skill
    strength = user.strength
    vitality = user.vitality

    atributy = {
        'HP': int(hp),
        'charisma': int(charisma),
        'dexterity': int(dexterity),
        'intelligence': int(intelligence),
        'skill': int(skill),
        'strength': int(strength),
        'vitality': int(vitality),
    }


    user.save()
    return atributy

def atributy_cena(request):

    user = atributy_funkce(request)
    hp = user['HP']
    charisma = user['charisma']
    dexterity = user['dexterity']
    intelligence = user['intelligence']
    skill = user['skill']
    strength = user['strength']
    vitality = user['vitality']

    charisma_price = charisma + (charisma * 1.5)
    dexterity_price = dexterity + (dexterity * 1.5)
    intelligence_price = intelligence + (intelligence * 1.5)
    skill_price = skill + (skill * 1.5)
    strength_price = strength + (strength * 1.5)
    vitality_price = vitality + (vitality * 1.5)

    cena = {
        'charisma_price': int(charisma_price),
        'dexterity_price': int(dexterity_price),
        'intelligence_price': int(intelligence_price),
        'skill_price': int(skill_price),
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




