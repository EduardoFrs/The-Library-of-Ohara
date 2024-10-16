from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UserRegistrationForm
from .models import Category
from .api import fetch_anime_by_id, fetch_anime_list, fetch_manga_by_id, fetch_manga_list, movie_list, serie_list
import json



"""Main pages for each categories"""
def index(request):
    return render(request, 'index.html')

def manga(request):
    page = request.GET.get('page', 1)
    manga_data = fetch_manga_list(page=int(page))
    return render(request, 'mainPages/manga.html', {'manga_page': manga_data})

def anime(request):
    page = request.GET.get('page', 1)
    anime_data = fetch_anime_list(page=int(page))
    return render(request, 'mainPages/anime.html', {'anime_page': anime_data})

def serie(request):
    series = serie_list(request)
    return render(request, 'mainPages/serie.html', {'series': series})

def movie(request):
    movies = movie_list(request)
    return render(request, 'mainPages/movie.html', {'movies': movies})




def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful.')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def create_category(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        category_name = data.get('category_name')
        if category_name:
            Category.objects.create(user=request.user, name=category_name)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'No category name provided.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


def anime_detail(request, anime_id):
    anime_data = fetch_anime_by_id(anime_id)
    return render(request, 'anime_details.html', {'anime': anime_data})

def manga_detail(request, manga_id):
    manga_data = fetch_manga_by_id(manga_id)
    return render(request, 'manga_details.html', {'manga': manga_data})

