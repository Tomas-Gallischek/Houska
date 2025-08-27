from .utils import atributy_hodnota
import random

def fight_off(request):
    user = request.user

    # INFORMACÉ O HRÁČI
    lvl = user.lvl
    hp = user.hp
    dmg_atribut = user.dmg_atribut

    # ATRIBUTY POSTAVY (pouze výpis)
    strength = user.strength # fizické poškození + fyzická obrana
    dexterity = user.dexterity # obratnost + vyhýbání
    intelligence = user.intelligence # magické poškození + magická obrana
    luck = user.luck  # Šance na kritický zásah
    vitality = user.vitality # Odolnost proti kritickým zásahům
    charisma = user.charisma # Šance na první úder

    # ZBRAŇ (DOVYTVOŘIT)
    #weapon = user.weapon
    weapon_dmg_min = 1
    weapon_dmg_max = 3

    # Útok
    if dmg_atribut == "strength":
        base_dmg = strength
    elif dmg_atribut == "intelligence":
        base_dmg = intelligence
    else:
        base_dmg = 0

    min_dmg = base_dmg * weapon_dmg_min
    max_dmg = base_dmg * weapon_dmg_max
    center_dmg = (min_dmg + max_dmg) // 2