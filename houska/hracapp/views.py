from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import CustomUser
from django.contrib import messages
import datetime
from django.utils import timezone


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages


def calculate_xp_and_level(orders):
    XP_aktual = orders
    lvl_aktual = 1
    lvl_next = 2
    XP_potrebne_next = round(100 + (lvl_aktual ** 2.2))

    for lvl in range(1, 100):
        XP_potrebne = round(100 + (lvl ** 2.2))
        if XP_aktual >= XP_potrebne:
            XP_aktual -= XP_potrebne
            lvl_aktual += 1
            lvl_next = lvl_aktual + 1
            XP_potrebne_next = round(100 + ((lvl + 1) ** 2.2))
        else:
            break

    return XP_aktual, lvl_aktual, lvl_next, XP_potrebne_next


def calculate_gold(user, lvl_aktual):
    # Koeficient růstu goldů
    if user.gold_growth_coefficient is not None:
        if lvl_aktual == 1:
            gold_growth_coefficient = 1
        else:
            gold_growth_coefficient = 1 + (lvl_aktual / 2)
        user.gold_growth_coefficient = gold_growth_coefficient
        user.save()
    else:
        gold_growth_coefficient = 1

    # VÝPOČET NASBÍRANÝCH GOLDŮ
    time_since_last_collection = timezone.now() - user.last_gold_collection
    seconds_since_last_collection = time_since_last_collection.total_seconds()

    collected_gold = min(int(seconds_since_last_collection), 28800) * gold_growth_coefficient
    gold_per_hour = round(gold_growth_coefficient * 3600)
    gold_limit = gold_per_hour * 8  # Limit pro zobrazení

    return collected_gold, gold_growth_coefficient, gold_limit, gold_per_hour


def render_profile(request, context):
    return render(request, 'hracapp/profile.html', context)


@login_required
def profile(request):

    # Pokud uživatel nemá žádné objednávky
    if request.user.orders is None:
        request.user.orders = 1
        request.user.save()

    # Výpočet XP a levelu
    XP_aktual, lvl_aktual, lvl_next, XP_potrebne_next = calculate_xp_and_level(request.user.orders)

    # Výpočet goldů
    collected_gold, gold_growth_coefficient, gold_limit, gold_per_hour = calculate_gold(request.user, lvl_aktual)

    # POST formuláře
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'collect_gold':
            request.user.gold += collected_gold
            request.user.last_gold_collection = timezone.now()
            request.user.save()
            messages.success(request, 'Goldy úspěšně sebrány!')
            return redirect('profile-url')

        elif action == 'update_orders':
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
    }

    return render_profile(request, context)


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
