from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from .models import Playerinfo
from .utils import calculate_xp_and_level, calculate_gold, atributy_funkce

@login_required
def profile(request):

    # Volání funkce pro LVL
    XP_aktual, lvl_aktual, lvl_next, XP_potrebne_next = calculate_xp_and_level(request.user.steps)

    # Volání funkce pro Gold
    collected_gold, gold_growth_coefficient, gold_limit, gold_per_hour = calculate_gold(request.user, lvl_aktual)

    # Volání funkce pro atributy
    atributy = atributy_funkce(request)

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