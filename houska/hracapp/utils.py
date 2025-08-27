from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Playerinfo


def atributy_funkce(request):
    # Získání atributů uživatele
    user = request.user
    atributy = {
        'HP': user.HP,
        'charisma': user.charisma,
        'dexterity': user.dexterity,
        'intelligence': user.intelligence,
        'skill': user.skill,
        'strength': user.strength,
        'vitality': user.vitality,
    }
    return atributy


def calculate_xp_and_level(steps):
    if steps is None:
        steps = 0
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

    return round(collected_gold,2), round(gold_growth_coefficient,2), round(gold_limit,2), round(gold_per_hour,2)




