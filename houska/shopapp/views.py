import json
from urllib import request
from django import utils
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from hracapp import views
from itemsapp import weapons

user = views.profile(request)
result = weapons.weapons_generator(user)
