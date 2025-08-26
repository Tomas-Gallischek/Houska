from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import CustomUser
from django.contrib import messages
import datetime
from django.utils import timezone


@login_required
def profile(request):

# IMPORT OBJEDNÁVEK Z DATABÁZE
    if request.user.orders is None:
        request.user.orders = 1
        request.user.save()

# VÝPOČET XP A LVL
    XP_aktual = request.user.orders
    lvl_aktual = 1

    for lvl in range(1, 100):
        XP_potrebne = round(100 + (lvl ** 2.2))
        if XP_aktual >= XP_potrebne:
            XP_aktual -= XP_potrebne
            lvl_aktual += 1
            lvl_next = lvl_aktual + 1
            XP_potrebne_next = round(100 + ((lvl+1) ** 2.2))
        else:
            break

# GOLDY A OBJEDNÁVKY

    # VÝPOČET NASBÍRANÝCH GOLDŮ
    time_since_last_collection = timezone.now() - request.user.last_gold_collection
    seconds_since_last_collection = time_since_last_collection.total_seconds()
    
    # Nasbírané goldy s limitem 28 800 sekund (8 hodin)
    collected_gold = min(int(seconds_since_last_collection), 28800) * request.user.gold_grow

    #FORMULÁŘE
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'collect_gold':
            request.user.gold += collected_gold
            request.user.last_gold_collection = timezone.now()
            request.user.save()
            messages.success(request, 'Goldy úspěšně sebrány!')
            return redirect('profile-url')
        elif action == 'update_orders':
            # Původní logika pro aktualizaci objednávek
            try:
                new_orders = int(request.POST.get('orders'))
                if new_orders is not None:
                    if new_orders >= request.user.orders:
                        request.user.orders = new_orders
                        request.user.save()
                        messages.success(request, 'Úspěšně AKTUALIZOVÁNO')
                    else:
                        messages.error(request, 'Zadaná hodnota nemůže být menší než aktuální.')
                else:
                    messages.error(request, 'Nezadali jste hodnotu objednávek.')
            except (ValueError, TypeError):
                pass
            
            return redirect('profile-url')


# ZÁVĚREČNÝ RENDER STRÁNKY
    return render(request, 'hracapp/profile.html', {
        'XP_aktual': XP_aktual,
        'lvl_aktual': lvl_aktual,
        'lvl_next': lvl_next,
        'XP_potrebne_next': XP_potrebne_next,
        'collected_gold': collected_gold,

    })

@login_required
def protected_page(request):
    return render(request, 'hracapp/protected-page.html')

def index(request):
    return render(request, 'hracapp/index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile-url')
    else:
        form = RegistrationForm()
    return render(request, 'hracapp/register.html', {'form': form})
