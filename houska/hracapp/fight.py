from . utils import atributy_funkce

def fight_off(request):
    user = request.user
    atributy = atributy_funkce(request)

    hp = atributy['HP']

    strength = atributy['strength']
    dexterity = atributy['dexterity']
    intelligence = atributy['intelligence']
    skill = atributy['skill']
    vitality = atributy['vitality']
    charisma = atributy['charisma']

    dmg_atribut = intelligence

    off_nubmer = dmg_atribut


