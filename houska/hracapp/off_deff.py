from .utils import atributy_hodnota
import random

def iniciace(request):
    user = request.user
    inicial_number = round((user.suma_charisma * 4) / (user.lvl), 2) # <-- % ŠANCE NA INICIATIVU (maximální honota 100 tj. 100%)
    if inicial_number > 100:
        inicial_number = 100
    return inicial_number

def fight_off(request):
    user = request.user

    # INFORMACÉ O HRÁČI
    lvl = user.lvl
    rasa = user.rasa
    povolani = user.povolani
    dmg_atribut = user.dmg_atribut

    # ATRIBUTY POSTAVY (pouze výpis)
    strength = user.suma_strength # POŠKOZENÍ TĚŽKÝMI ZBRANĚMI
    dexterity = user.suma_dexterity # POŠKOZENÍ LEHKÝMI ZBRANĚMI
    intelligence = user.suma_intelligence # POŠKOZENÍ MAGICKÝMI ZBRANĚMI
    luck = user.suma_luck  # ŠANCE NA KRITICKÝ ZÁSAH

    # ZBRAŇ (DOVYTVOŘIT)
    #weapon = user.weapon
    #weapon_typ = user.weapon_typ
    weapon_typ = "heavy" # < -- pracovní
    weapon_dmg_min = 1
    weapon_dmg_max = 3

    # Útok
    if weapon_typ == "heavy":
        base_dmg = strength
    elif weapon_typ == "magic":
        base_dmg = intelligence
    elif weapon_typ == "light":
        base_dmg = dexterity
    else:
        base_dmg = (min_dmg + max_dmg) // 2

    min_dmg = base_dmg * weapon_dmg_min
    max_dmg = base_dmg * weapon_dmg_max
    center_dmg = (min_dmg + max_dmg) // 2

    crit_chance = (luck / 2) / (user.lvl / 3)
    if crit_chance >= 50:
        crit_chance = 50
    if crit_chance < 1:
        crit_chance = 1

    return crit_chance, center_dmg, min_dmg, max_dmg, weapon_typ

def fight_def(request):
    user = request.user

    # INFORMACÉ O HRÁČI
    lvl = user.lvl
    rasa = user.rasa
    povolani = user.povolani

    # ATRIBUTY POSTAVY (pouze výpis)
    strength = user.suma_strength # REZISTENCE PROTI TĚŽKÝM ZBRANÍM
    intelligence = user.suma_intelligence # REZISTENCE PROTI MAGICKÝM ZBRANÍM
    dexterity = user.suma_dexterity # REZISTENCE PROTI LEHKÝM ZBRANÍM
    luck = user.suma_luck  # ŠANCE NA ÚHYB

    # ZBROJ (DOVYTVOŘIT)
    #armor = user.armor

    heavy_res = round(strength // 10, 2)
    magic_res = round(intelligence // 10, 2)
    light_res = round(dexterity // 10, 2)

    dodge_chance = round(((luck / 2) / (user.lvl / 3)) / 2, 2)

    return heavy_res, magic_res, light_res, dodge_chance