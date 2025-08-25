from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def index(request):
    return render(request, 'hracapp/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login-url')
    else:
        form = CustomUserCreationForm()
        
    # Tento řádek zajistí, že se formulář vyrenderuje
    # jak v případě GET požadavku, tak v případě
    # nevalidního POST požadavku (s chybovými hlášeními).
    return render(request, 'hracapp/register.html', {'form': form})

def profile(request):
    return render(request, 'hracapp/profile.html')

def protected_page(request):
    return render(request, 'hracapp/protected-page.html')