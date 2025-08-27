import json
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Playerinfo
from django.http import JsonResponse
from .utils import atributy_cena, calculate_xp_and_level, calculate_gold, atributy_funkce

@login_required
def profile(request):

    # Volání funkce pro LVL
    XP_aktual, lvl_aktual, lvl_next, XP_potrebne_next = calculate_xp_and_level(request)

    # Volání funkce pro Gold
    collected_gold, gold_growth_coefficient, gold_limit, gold_per_hour = calculate_gold(request.user, lvl_aktual)

    # Volání funkce pro atributy
    atributy = atributy_funkce(request)

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
        'cena_skill': cena_atributu['skill_price'],
        'cena_strength': cena_atributu['strength_price'],
        'cena_vitality': cena_atributu['vitality_price'],

    }

    return render_profile(request, context)


@login_required
def protected_page(request):
    return render(request, 'hracapp/protected-page.html')

def index(request):
    return render(request, 'hracapp/index.html')

def register(request):

    #REGISTRAČNÍ FORMULÁŘ
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
            
            # Zkontroluje, zda je atribut platný a není to HP
            valid_attributes = ['strength', 'dexterity', 'intelligence', 'charisma', 'vitality', 'skill']
            if attribute_to_update in valid_attributes:

                # Odečtení ceny atributu z uživatelských goldů
                user = request.user
                old_prices = atributy_cena(request)
                atribut_bill = old_prices.get(f'{attribute_to_update}_price')
                user.gold -= atribut_bill
                user.save()
                new_golds = user.gold

                # Aktualizace atributu
                current_value = getattr(user, attribute_to_update)
                setattr(user, attribute_to_update, current_value + 1)
                user.save()

                # Vypočítá nové ceny atributů
                new_prices = atributy_cena(request)


                return JsonResponse({'success': True, 'new_value': current_value + 1, 'new_prices': new_prices, 'new_golds': new_golds})
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