from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'hracapp/index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login-url')
    else:
        form = RegistrationForm()
    return render(request, 'hracapp/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'hracapp/profile.html')

@login_required
def protected_page(request):
    return render(request, 'hracapp/protected-page.html')