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

    # Ofenzivní a defenzivní statistiky
    crit_chance, center_dmg, min_dmg, max_dmg, weapon_typ = fight_off(request)
    heavy_res, magic_res, light_res, dodge_chance = fight_def(request)
    inicial_number = iniciace(request)

    # Volání funkce pro LVL
    XP_aktual, lvl_aktual, lvl_next, XP_potrebne_next = calculate_xp_and_level(request)

    # Volání funkce pro Gold
    collected_gold, gold_growth_coefficient, gold_limit, gold_per_hour = calculate_gold(request.user, lvl_aktual)

    # Volání funkce pro atributy
    atributy = atributy_hodnota(request)

    #volání funkce pro CENU ATRIBUTŮ
    cena_atributu = atributy_cena(request)

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
        'XP_aktual': XP_aktual,
        'lvl_aktual': lvl_aktual,
        'lvl_next': lvl_next,
        'XP_potrebne_next': XP_potrebne_next,
        'collected_gold': collected_gold,
        'gold_growth_coefficient': gold_growth_coefficient,
        'gold_limit': gold_limit,
        'gold_per_hour': gold_per_hour,
        'atributy': atributy,
        'cena_charisma': cena_atributu['charisma_price'],
        'cena_dexterity': cena_atributu['dexterity_price'],
        'cena_intelligence': cena_atributu['intelligence_price'],
        'cena_luck': cena_atributu['luck_price'],
        'cena_strength': cena_atributu['strength_price'],
        'cena_vitality': cena_atributu['vitality_price'],
        'heavy_res': heavy_res,
        'magic_res': magic_res,
        'light_res': light_res,
        'dodge_chance': dodge_chance,
        'crit_chance': crit_chance,
        'center_dmg': center_dmg,
        'weapon_typ': weapon_typ,
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
                atribut_bill = current_prices.get(f'{attribute_to_update}_price')

                # Kontrola dostatku goldů
                if user.gold < atribut_bill:
                    return JsonResponse({'success': False, 'error': 'Nedostatek zlata.'})

                # Odečtení ceny atributu z uživatelských goldů a uložení
                user.gold -= atribut_bill
                user.save()

                # Aktualizace atributu a uložení
                current_value = getattr(user, attribute_to_update)
                new_value = current_value + 1
                setattr(user, attribute_to_update, new_value)
                user.save()

                # Vypočítá nové ceny a hodnoty atributů po aktualizaci
                new_prices = atributy_cena(request)
                atributy = atributy_hodnota(request)

                # Sestavení a vrácení odpovědi
                response_data = {
                    'success': True,
                    'new_value': new_value,
                    'new_prices': new_prices,
                    'new_golds': user.gold,
                    'new_hp': atributy['HP']
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