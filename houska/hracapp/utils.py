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

    # ŽIVOTY
    base_hp = 10
    hp_bonus_rasa = user.hp_bonus
    hp_bonus_vitality = user.suma_vitality * 0.1
    plus_hp = 1 * hp_bonus_rasa * hp_bonus_vitality
    suma_hp = (base_hp * hp_bonus_rasa) * ((100 + hp_bonus_vitality)/100)

    # URČENÍ ZÁKLADNÍCH ATRIBUTŮ a jejich zpětné uložení (nic se nemění)
    base_strength = user.strength_base
    base_dexterity = user.dexterity_base
    base_intelligence = user.intelligence_base
    base_charisma = user.charisma_base
    base_vitality = user.vitality_base
    base_luck = user.luck_base
    user.save()

    # URČENÍ A ULOŽENÍ HODNOTY ATRIBUTŮ (plus)
    plus_strength = user.strength_plus
    plus_dexterity = user.dexterity_plus
    plus_intelligence = user.intelligence_plus
    plus_charisma = user.charisma_plus
    plus_vitality = user.vitality_plus
    plus_luck = user.luck_plus
    user.save()

    # DEFINITIVNÍ HODNOTA ATRIBUTŮ (základ + hodnota v databázi)

    suma_strength = base_strength + plus_strength
    suma_dexterity = base_dexterity + plus_dexterity
    suma_intelligence = base_intelligence + plus_intelligence
    suma_charisma = base_charisma + plus_charisma
    suma_vitality = base_vitality + plus_vitality
    suma_luck = base_luck + plus_luck
    user.suma_strength = suma_strength
    user.suma_dexterity = suma_dexterity
    user.suma_intelligence = suma_intelligence
    user.suma_charisma = suma_charisma
    user.suma_vitality = suma_vitality
    user.suma_luck = suma_luck
    user.save()

    base_atributy = {
        "base_hp": base_hp,
        "base_strength": base_strength,
        "base_dexterity": base_dexterity,
        "base_intelligence": base_intelligence,
        "base_charisma": base_charisma,
        "base_vitality": base_vitality,
        "base_luck": base_luck
    }

    plus_atributy = {
        "plus_hp": plus_hp,
        "plus_strength": plus_strength,
        "plus_dexterity": plus_dexterity,
        "plus_intelligence": plus_intelligence,
        "plus_charisma": plus_charisma,
        "plus_vitality": plus_vitality,
        "plus_luck": plus_luck
    }

    suma_atributy = {
        "suma_hp":  suma_hp,
        "suma_strength":  suma_strength,
        "suma_dexterity": suma_dexterity,
        "suma_intelligence": suma_intelligence,
        "suma_charisma": suma_charisma,
        "suma_vitality": suma_vitality,
        "suma_luck": suma_luck
    }

    return suma_atributy, base_atributy, plus_atributy, plus_strength, plus_dexterity, plus_intelligence, plus_charisma, plus_vitality, plus_luck

@login_required
def atributy_cena(request):
    plus_strength, plus_dexterity, plus_intelligence, plus_charisma, plus_vitality, plus_luck = atributy_hodnota(request)


    strength_cost = plus_strength * 1.5
    dexterity_cost = plus_dexterity * 1.5
    intelligence_cost = plus_intelligence * 1.5
    vitality_cost = plus_vitality * 1.5
    luck_cost = plus_luck * 1.5
    charisma_cost = plus_charisma * 1.5

    atributy_cost = {
        "strength_cost":  strength_cost,
        "dexterity_cost":  dexterity_cost,
        "intelligence_cost":  intelligence_cost,
        "charisma_cost":  charisma_cost,
        "vitality_cost":  vitality_cost,
        "luck_cost":  luck_cost,
    }

    return atributy_cost


def calculate_xp_and_level(request):
    user = request.user
    steps = user.steps if user.steps is not None else 0
    XP_aktual = steps
    lvl_aktual = 1
    lvl_next = 2
    XP_potrebne_next = round((22 * lvl_aktual) * ((lvl_next) * 1.1))

    for lvl in range(1, 500):
        XP_potrebne = round((22 * lvl) * ((lvl**1.1)))
        if XP_aktual >= XP_potrebne:
            XP_aktual -= XP_potrebne
            lvl_aktual += 1
            lvl_next = lvl_aktual + 1
            XP_potrebne_next = round((22 * lvl_next) * ((lvl_next**1.1)))
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
    return round(collected_gold, 2), round(gold_growth_coefficient, 2), round(gold_limit, 2), round(gold_per_hour, 2)