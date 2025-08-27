from urllib import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

@login_required
def povolani_bonus(request):

    # SÍLA (DMG -> MID -> TANK)
    if request.user.povolani == 'Paladin' or request.user.povolani == 'paladin':
        dmg_atribut = 'strength'
    elif request.user.povolani == 'Válečník' or request.user.povolani == 'warrior':
        dmg_atribut = 'strength'
        dmg_atribut = 'strength'
    elif request.user.povolani == 'Ničitel' or request.user.povolani == 'berserker':
        dmg_atribut = 'strength'

    # INTELIGENCE (DMG -> MID -> TANK (heal))
    elif request.user.povolani == 'Mág' or request.user.povolani == 'mage':
        dmg_atribut = 'intelligence'
    elif request.user.povolani == 'Nekromant' or request.user.povolani == 'necromancer':
        dmg_atribut = 'intelligence'
        dmg_atribut = 'intelligence'
    elif request.user.povolani == 'Druid' or request.user.povolani == 'druid':
        dmg_atribut = 'intelligence'

    # OBRATNOST (DMG -> MID -> TANK)
    elif request.user.povolani == 'Roguna' or request.user.povolani == 'rogue':
        dmg_atribut = 'dexterity'
    elif request.user.povolani == 'Hraničář' or request.user.povolani == 'ranger':
        dmg_atribut = 'dexterity'
    elif request.user.povolani == 'Mnich' or request.user.povolani == 'monk':
        dmg_atribut = 'dexterity'

    else:
        print(" ! NEVYBRALO SE ŽÁDNÉ POVOLÁNÍ !")
    request.user.dmg_atribut = dmg_atribut
    request.user.save()







@login_required
def rasa_bonus(request):

    koeficient_statu = 3 # JEŠTĚ NEVÍM KOLIK PŘESNĚ BUDOU ZÁKLADNÍ STATY. PÍŠU TO CO BYL ORIGINÁL A PŘÍPADNĚ TO NÁSOBÍM

    if request.user.rasa == 'Člověk' or request.user.rasa == 'human':
        # OBECNÉ BONUSY
        hp_bonus = 1
        # ZÁKLADNÍ STATY
        strength_bonus = 5 * koeficient_statu
        vitality_bonus = 4 * koeficient_statu
        dexterity_bonus = 4 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 5 * koeficient_statu
        luck_bonus = 3 * koeficient_statu

    elif request.user.rasa == 'Elf' or request.user.rasa == 'elf':
        # OBECNÉ BONUSY
        hp_bonus = 0.8
        # ZÁKLADNÍ STATY
        strength_bonus = 3 * koeficient_statu
        vitality_bonus = 3 * koeficient_statu
        dexterity_bonus = 5 * koeficient_statu
        intelligence_bonus = 7 * koeficient_statu
        charisma_bonus = 4 * koeficient_statu
        luck_bonus = 3 * koeficient_statu

    elif request.user.rasa == 'Trpaslík' or request.user.rasa == 'dwarf':
        # OBECNÉ BONUSY
        hp_bonus = 1.2
        # ZÁKLADNÍ STATY
        strength_bonus = 4 * koeficient_statu
        vitality_bonus = 5 * koeficient_statu
        dexterity_bonus = 3 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 3 * koeficient_statu
        luck_bonus = 6 * koeficient_statu  

    elif request.user.rasa == 'Urgal' or request.user.rasa == 'urgal':
        # OBECNÉ BONUSY
        hp_bonus = 1.3
        # ZÁKLADNÍ STATY
        strength_bonus = 5 * koeficient_statu
        vitality_bonus = 9 * koeficient_statu
        dexterity_bonus = 3 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 2 * koeficient_statu
        luck_bonus = 2 * koeficient_statu

    elif request.user.rasa == 'Gnóm' or request.user.rasa == 'gnome':
        # OBECNÉ BONUSY
        hp_bonus = 1
        # ZÁKLADNÍ STATY
        strength_bonus = 4 * koeficient_statu
        vitality_bonus = 4 * koeficient_statu
        dexterity_bonus = 4 * koeficient_statu
        intelligence_bonus = 5 * koeficient_statu
        charisma_bonus = 2 * koeficient_statu
        luck_bonus = 5 * koeficient_statu

    elif request.user.rasa == 'Stín' or request.user.rasa == 'shadow':
        # OBECNÉ BONUSY
        hp_bonus = 0.7
        # ZÁKLADNÍ STATY
        strength_bonus = 3 * koeficient_statu
        vitality_bonus = 2 * koeficient_statu
        dexterity_bonus = 10 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 2 * koeficient_statu
        luck_bonus = 4 * koeficient_statu
    else:
        print(" ! NEVYBRALA SE ŽÁDNÁ RASA !")

    request.user.hp_bonus = float(hp_bonus)
    request.user.strength_base = float(strength_bonus)
    request.user.vitality_base = float(vitality_bonus)
    request.user.dexterity_base = float(dexterity_bonus)
    request.user.intelligence_base = float(intelligence_bonus)
    request.user.charisma_base = float(charisma_bonus)
    request.user.luck_base = float(luck_bonus)
    request.user.save()

    rasa_bonus = (
        hp_bonus + strength_bonus + vitality_bonus + dexterity_bonus + intelligence_bonus + charisma_bonus + luck_bonus
    )
    return rasa_bonus