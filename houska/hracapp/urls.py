from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register-url'),
    path('login', auth_views.LoginView.as_view(template_name='hracapp/login.html'), name='login-url'),
    path('logout', auth_views.LogoutView.as_view(template_name='hracapp/logout.html'), name='logout-url'),
    path('profile', views.profile, name='profile-url'),
    path('protected-page', views.protected_page, name='protected-page-url'),
    path('update-steps', views.update_steps, name='update-steps-url'),
    path('gold_per_second', views.gold_per_second, name='views-data-url'),  # Přidána URL pro získání dat z views.py
    path('upgrade-attribute/', views.upgrade_attribute, name='upgrade-attribute-url'),
    ]