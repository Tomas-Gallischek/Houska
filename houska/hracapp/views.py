from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import CustomUser
from django.contrib import messages


@login_required
def profile(request):

# IMPORT OBJEDNÁVEK Z DATABÁZE
    if request.user.orders is None:
        request.user.orders = 1
        request.user.save()

# AKTUALIZACE OBJEDNÁVEK
    if request.method == 'POST':
        try:
            new_orders = int(request.POST.get('orders'))
            if new_orders is not None:
                if new_orders >= request.user.orders:
                    request.user.orders = new_orders
                    request.user.save()
                    messages.success(request, 'Úspěšně AKTUALIZOVÁNO') # Úspěšná zpráva
                else:
                    messages.error(request, 'Zadaná hodnota nemůže být menší než aktuální.') # Chybová zpráva
            else:
                messages.error(request, 'Nezadali jste hodnotu objednávek.') # Chybová zpráva
        except (ValueError, TypeError):
            messages.error(request, 'Zadali jste neplatnou hodnotu.') # Chybová zpráva
        
        return redirect('profile-url')

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

# VÝPOČET GOLDŮ
    gold_aktual = CustomUser.objects.get(id=request.user.id).gold


# ZÁVĚREČNÝ RENDER STRÁNKY
    return render(request, 'hracapp/profile.html', {
        'XP_aktual': XP_aktual,
        'lvl_aktual': lvl_aktual,
        'lvl_next': lvl_next,
        'XP_potrebne_next': XP_potrebne_next
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
