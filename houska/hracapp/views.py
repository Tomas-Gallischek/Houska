from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import CustomUser


def index(request):
    return render(request, 'hracapp/index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Přihlásí uživatele automaticky po registraci
            return redirect('profile-url')
    else:
        form = RegistrationForm()
    return render(request, 'hracapp/register.html', {'form': form})

@login_required
def profile(request):
    if request.user.orders is None:
        request.user.orders = 1
        request.user.save()

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


    return render(request, 'hracapp/profile.html', {
        'XP_aktual': XP_aktual,
        'lvl_aktual': lvl_aktual,
        'lvl_next': lvl_next,
        'XP_potrebne_next': XP_potrebne_next
    })

@login_required
def protected_page(request):
    return render(request, 'hracapp/protected-page.html')