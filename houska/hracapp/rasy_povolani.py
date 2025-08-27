def rasa_bonus(request):
    user = request.user
    rasa_bonus = 0
    koeficient_statu = 3 # JEŠTĚ NEVÍM KOLIK PŘESNĚ BUDOU ZÁKLADNÍ STATY. PÍŠU TO CO BYL ORIGINÁL A PŘÍPADNĚ TO NÁSOBÍM

    if user.rasa == 'human' or user.rasa == 'Člověk':
        # OBECNÉ BONUSY
        hp_bonus = 1
        # ZÁKLADNÍ STATY
        strength_bonus = 5 * koeficient_statu
        vitality_bonus = 4 * koeficient_statu
        dexterity_bonus = 4 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 5 * koeficient_statu
        skill_bonus = 3 * koeficient_statu

    elif user.rasa == 'elf' or user.rasa == 'Elf':
        # OBECNÉ BONUSY
        hp_bonus = 0.8
        # ZÁKLADNÍ STATY
        strength_bonus = 3 * koeficient_statu
        vitality_bonus = 3 * koeficient_statu
        dexterity_bonus = 5 * koeficient_statu
        intelligence_bonus = 7 * koeficient_statu
        charisma_bonus = 4 * koeficient_statu
        skill_bonus = 3 * koeficient_statu

    elif user.rasa == 'dwarf' or user.rasa == 'Trpaslík':
        # OBECNÉ BONUSY
        hp_bonus = 1.2
        # ZÁKLADNÍ STATY
        strength_bonus = 4 * koeficient_statu
        vitality_bonus = 5 * koeficient_statu
        dexterity_bonus = 3 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 3 * koeficient_statu
        skill_bonus = 6 * koeficient_statu  

    elif user.rasa == 'urgal' or user.rasa == 'Urgal':
        # OBECNÉ BONUSY
        hp_bonus = 1.3
        # ZÁKLADNÍ STATY
        strength_bonus = 5 * koeficient_statu
        vitality_bonus = 9 * koeficient_statu
        dexterity_bonus = 3 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 2 * koeficient_statu
        skill_bonus = 2 * koeficient_statu

    elif user.rasa == 'gnóm' or user.rasa == 'Gnóm':
        # OBECNÉ BONUSY
        hp_bonus = 1
        # ZÁKLADNÍ STATY
        strength_bonus = 4 * koeficient_statu
        vitality_bonus = 4 * koeficient_statu
        dexterity_bonus = 4 * koeficient_statu
        intelligence_bonus = 5 * koeficient_statu
        charisma_bonus = 2 * koeficient_statu
        skill_bonus = 5 * koeficient_statu

    elif user.rasa == 'shadow' or user.rasa == 'Stín':
        # OBECNÉ BONUSY
        hp_bonus = 0.7
        # ZÁKLADNÍ STATY
        strength_bonus = 3 * koeficient_statu
        vitality_bonus = 2 * koeficient_statu
        dexterity_bonus = 10 * koeficient_statu
        intelligence_bonus = 3 * koeficient_statu
        charisma_bonus = 2 * koeficient_statu
        skill_bonus = 4 * koeficient_statu

    request.user.HP_bonus = float(hp_bonus)
    request.user.strength_base = float(strength_bonus)
    request.user.vitality_base = float(vitality_bonus)
    request.user.dexterity_base = float(dexterity_bonus)
    request.user.intelligence_base = float(intelligence_bonus)
    request.user.charisma_base = float(charisma_bonus)
    request.user.skill_base = float(skill_bonus)
    request.user.save()

    rasa_bonus = (
        hp_bonus + strength_bonus + vitality_bonus + dexterity_bonus + intelligence_bonus + charisma_bonus + skill_bonus
    )
    return rasa_bonus