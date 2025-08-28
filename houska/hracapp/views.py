import json
from urllib import request
from django import utils
from django.shortcuts import render, redirect
from .off_deff import fight_def, fight_off, iniciace
from .rasy_povolani import povolani_bonus, rasa_bonus
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Playerinfo
from django.http import JsonResponse
from .utils import calculate_xp_and_level, calculate_gold, atributy_hodnota, atributy_cena


@login_required
def profile(request):
    # Inicializace RASY A POVOLÁNÍ
    povolani_bonus(request)
    rasa_bonus(request)

    # Volání funkce pro atributy
    suma_atributy, base_atributy, plus_atributy, plus_strength, plus_dexterity, plus_intelligence, plus_charisma, plus_vitality, plus_luck = atributy_hodnota(request)

    # Volání funkce pro cenu atributů
    atributy_cost = atributy_cena(request)

    # Volání funkce pro LVL
    XP_aktual, lvl_aktual, lvl_next, XP_potrebne_next  = calculate_xp_and_level(request)

    # Volání funkce pro Gold
    collected_gold, gold_growth_coefficient, gold_limit, gold_per_hour = calculate_gold(request.user, lvl_aktual)

    # Ofenzivní a defenzivní statistiky
    crit_chance, center_dmg, min_dmg, max_dmg, weapon_typ = fight_off(request)
    heavy_res, magic_res, light_res, dodge_chance = fight_def(request)
    inicial_number = iniciace(request)

    # POST formuláře
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'collect_gold':
            request.user.gold += collected_gold
            request.user.last_gold_collection = timezone.now()
            request.user.save()
            messages.success(request, 'Goldy úspěšně sebrány!')
            return redirect('profile-url')

    # Kontext pro render
    context = {
    # XP A LVL
        'XP_aktual': XP_aktual,
        'lvl_aktual': lvl_aktual,
        'lvl_next': lvl_next,
        'XP_potrebne_next': XP_potrebne_next,
    # GOLDY
        'collected_gold': collected_gold,
        'gold_growth_coefficient': gold_growth_coefficient,
        'gold_limit': gold_limit,
        'gold_per_hour': gold_per_hour,
    # ATRIBUTY - BASE
        'base_hp': base_atributy["base_hp"],
        'base_strength': base_atributy["base_strength"],
        'base_dexterity': base_atributy["base_dexterity"],
        'base_intelligence': base_atributy["base_intelligence"],
        'base_charisma': base_atributy["base_charisma"],
        'base_vitality': base_atributy["base_vitality"],
        'base_luck': base_atributy["base_luck"],
    # ATRIBUTY - PLUS
        'plus_hp': plus_atributy["plus_hp"],
        'plus_strength': plus_atributy["plus_strength"],
        'plus_dexterity': plus_atributy["plus_dexterity"],
        'plus_intelligence': plus_atributy["plus_intelligence"],
        'plus_charisma': plus_atributy["plus_charisma"],
        'plus_vitality': plus_atributy["plus_vitality"],
        'plus_luck': plus_atributy["plus_luck"],
    # ATRIBUTY - SUMA
        'suma_hp': suma_atributy["suma_hp"],
        'suma_strength': suma_atributy["suma_strength"],
        'suma_dexterity': suma_atributy["suma_dexterity"],
        'suma_intelligence': suma_atributy["suma_intelligence"],
        'suma_charisma': suma_atributy["suma_charisma"],
        'suma_vitality': suma_atributy["suma_vitality"],
        'suma_luck': suma_atributy["suma_luck"],
    # ATRIBUTY - CENA
        'strength_cost': atributy_cost["strength_cost"],
        'dexterity_cost': atributy_cost["dexterity_cost"],
        'intelligence_cost': atributy_cost["intelligence_cost"],
        'charisma_cost': atributy_cost["charisma_cost"],
        'vitality_cost': atributy_cost["vitality_cost"],
        'luck_cost': atributy_cost["luck_cost"],
    # OFF 
        'crit_chance': crit_chance,
        'center_dmg': center_dmg,
        'weapon_typ': weapon_typ,
    # DEF
        'heavy_res': heavy_res,
        'magic_res': magic_res,
        'light_res': light_res,
        'dodge_chance': dodge_chance,
    # OSTATNÍ
        'inicial_number': inicial_number,
    }

    return render_profile(request, context)


@login_required
def protected_page(request):
    return render(request, 'hracapp/protected-page.html')


def index(request):
    return render(request, 'hracapp/index.html')


def register(request):
    # REGISTRAČNÍ FORMULÁŘ
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile-url')
    else:
        form = RegistrationForm()
    return render(request, 'hracapp/register.html', {'form': form})


def render_profile(request, context):
    return render(request, 'hracapp/profile.html', context)


def update_steps(request):
    if request.method == 'POST':
        new_steps = request.POST.get('steps')
        if new_steps is not None:
            request.user.steps = new_steps
            request.user.save()
            messages.success(request, 'Kroky byly úspěšně aktualizovány.')
        else:
            messages.error(request, 'Nezadali jste platnou hodnotu kroků.')
    return render(request, 'hracapp/steps_input.html')


@login_required
def update_attribute(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            attribute_to_update = data.get('attribute')

            # Zkontroluje, zda je atribut platný
            valid_attributes = ['strength', 'dexterity', 'intelligence', 'charisma', 'vitality', 'luck']
            if attribute_to_update in valid_attributes:

                user = request.user

                # Získáme aktuální ceny
                current_prices = atributy_cena(request)
                atribut_bill = current_prices.get(f'{attribute_to_update}_cost')

                # Kontrola dostatku goldů
                if user.gold < atribut_bill:
                    return JsonResponse({'success': False, 'error': 'Nedostatek zlata.'})

                # Odečtení ceny atributu z uživatelských goldů a uložení
                else:
                    user.gold -= atribut_bill
                    user.save()

                # Aktualizace atributu a uložení
                print(f"attribute_to_update: {attribute_to_update}")
                if attribute_to_update == 'strength':
                    user.suma_strength += 1
                    new_value = user.suma_strength
                    user.save()
                if attribute_to_update == 'dexterity':
                    user.suma_dexterity += 1
                    new_value = user.suma_dexterity
                    user.save()
                if attribute_to_update == 'intelligence':
                    user.suma_intelligence += 1
                    new_value = user.suma_intelligence
                    user.save()
                if attribute_to_update == 'charisma':
                    user.suma_charisma += 1
                    new_value = user.suma_charisma
                    user.save()
                if attribute_to_update == 'vitality':
                    user.suma_vitality += 1
                    user.HP = user.suma_hp
                    new_value = user.suma_vitality
                    user.save()
                if attribute_to_update == 'luck':
                    user.suma_luck += 1
                    new_value = user.suma_luck
                    user.save()
                print(f"Byla vylepšena {attribute_to_update} na hodnotu {new_value}")


                # Vypočítá nové ceny a hodnoty atributů po aktualizaci
                new_prices = atributy_cena(request)

                # Sestavení a vrácení odpovědi
                response_data = {
                    'success': True,
                    'new_value': new_value,
                    'new_prices': new_prices,
                    'new_golds': user.gold,
                    'new_hp': user.HP,
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'success': False, 'error': 'Neplatný atribut.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Neplatná JSON data.'}, status=400)

    return JsonResponse({'success': False, 'error': 'Neplatná metoda požadavku.'}, status=405)


@login_required
def gold_per_second(request):
    lvl_aktual = calculate_xp_and_level(request)[1]
    golds_info = calculate_gold(request.user, lvl_aktual)
    collected_gold = golds_info[0]
    aktualizovana_hodnota = collected_gold

    # Vrácení dat jako JSON
    data = {
        'hodnota': aktualizovana_hodnota,
    }
    return JsonResponse(data)