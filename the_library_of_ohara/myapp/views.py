from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UserRegistrationForm
from .models import Category, Manga, Anime, Serie, Movie, UserMangaCollection, UserAnimeCollection, UserSerieCollection, UserMovieCollection
from .api import fetch_anime_by_id, fetch_anime_list, fetch_manga_by_id, fetch_manga_list, movie_list, serie_list
import json

""" Main functions """

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

@login_required
def user_category(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'index.html', {'categories': categories})



""" Main pages for each categories """

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

@login_required
def user_collection(request):
    user_manga_collection = UserMangaCollection.objects.filter(user=request.user)
    user_anime_collection = UserAnimeCollection.objects.filter(user=request.user)
    user_serie_collection = UserSerieCollection.objects.filter(user=request.user)
    user_movie_collection = UserMovieCollection.objects.filter(user=request.user)

    return render(request, 'userCategory/user_collection.html', {
        'user_manga_collection': user_manga_collection,
        'user_anime_collection': user_anime_collection,
        'user_serie_collection': user_serie_collection,
        'user_movie_collection': user_movie_collection,
    })


""" Manga """

@login_required
def user_manga_collection(request):
    user_manga = UserMangaCollection.objects.filter(user=request.user)
    available_manga = Manga.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        user_manga = user_manga.filter(user_status=status_filter)
    return render(request, 'userCategory/user_manga.html', {
        'user_manga': user_manga,
        'available_manga': available_manga,
    })

def manga_detail(request, manga_id):
    manga_data = fetch_manga_by_id(manga_id)
    return render(request, 'manga_details.html', {'manga': manga_data})

@login_required
def add_manga_to_collection(request, manga_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        manga = Manga.objects.get(api_id=manga_id)
        user_status = data.get('user_status')
        current_chapter = data.get('current_chapter')

        user_manga_collection, created = UserMangaCollection.objects.get_or_create(user=request.user, manga=manga)

        user_manga_collection.user_status = user_status
        if user_status in ['currently', 'pause']:
            user_manga_collection.current_chapter = current_chapter
        else:
            user_manga_collection.current_chapter = None

        user_manga_collection.save()

        return JsonResponse({'success': True, 'message': 'Manga added to collection with user status: ' + user_status})

@login_required
def remove_manga_from_collection(request, manga_id):
    user_manga = get_object_or_404(UserMangaCollection, id=manga_id, user=request.user)
    user_manga.delete()
    messages.success(request, 'Manga removed from your collection.')
    return redirect('user_manga')

def manga_list(request):
    page = request.GET.get('page', 1)
    per_page = 50

    manga_data = fetch_manga_list(page=int(page), per_page=per_page)

    if manga_data:
        mangas = []
        for media in manga_data['media']:
            mangas.append({
                'id': media['id'],
                'title': media['title']['english'],
                'cover_image': media['coverImage']['large'],
            })
        return JsonResponse(mangas, safe=False)
    else:
        return JsonResponse([], safe=False)



""" Anime """

@login_required
def user_anime_collection(request):
    user_anime = UserAnimeCollection.objects.filter(user=request.user)
    available_anime = Anime.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        user_anime = user_anime.filter(user_status=status_filter)
    return render(request, 'userCategory/user_anime.html', {
        'user_anime': user_anime,
        'available_anime': available_anime,
    })

def anime_detail(request, anime_id):
    anime_data = fetch_anime_by_id(anime_id)
    return render(request, 'anime_details.html', {'anime': anime_data})

@login_required
def add_anime_to_collection(request, anime_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        anime = Anime.objects.get(api_id=anime_id)
        user_status = data.get('user_status')
        current_episode = data.get('current_episode')

        user_anime_collection, created = UserAnimeCollection.objects.get_or_create(user=request.user, anime=anime)

        user_anime_collection.user_status = user_status
        if user_status in ['currently', 'pause']:
            user_anime_collection.current_episode = current_episode
        else:
            user_anime_collection.current_episode = None

        user_anime_collection.save()

        return JsonResponse({'success': True, 'message': 'Anime added to collection with user status: ' + user_status})

@login_required
def remove_anime_from_collection(request, anime_id):
    user_anime = get_object_or_404(UserAnimeCollection, id=anime_id, user=request.user)
    user_anime.delete()
    messages.success(request, 'Anime removed from your collection.')
    return redirect('user_anime')

def anime_list(request):
    page = request.GET.get('page', 1)
    per_page = 50

    anime_data = fetch_anime_list(page=int(page), per_page=per_page)

    if anime_data:
        animes = []
        for media in anime_data['media']:
            animes.append({
                'id': media['id'],
                'title': media['title']['english'],
                'cover_image': media['coverImage']['large'],
            })
        return JsonResponse(animes, safe=False)
    else:
        return JsonResponse([], safe=False)



""" Serie """

@login_required
def user_serie_collection(request):
    user_series = UserSerieCollection.objects.filter(user=request.user)
    available_serie = Serie.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        user_series = user_series.filter(user_status=status_filter)
    return render(request, 'userCategory/user_serie.html', {
        'user_serie': user_series,
        'available_serie': available_serie,
        })

def serie_detail(request, serie_id):
    serie = get_object_or_404(Serie, id=serie_id)
    return render(request, 'serie_details.html', {'serie': serie})

@login_required
def add_serie_to_collection(request, serie_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        serie = Serie.objects.get(api_id=serie_id)
        user_status = data.get('user_status')
        current_episode = data.get('current_episode')

        user_serie_collection, created = UserSerieCollection.objects.get_or_create(user=request.user, serie=serie)

        user_serie_collection.user_status = user_status
        if user_status in ['currently', 'pause']:
            user_serie_collection.current_episode = current_episode
        else:
            user_serie_collection.current_episode = None

        user_serie_collection.save()

        return JsonResponse({'success': True, 'message': 'Serie added to collection with user status: ' + user_status})

@login_required
def remove_serie_from_collection(request, serie_id):
    user_serie = get_object_or_404(UserSerieCollection, id=serie_id, user=request.user)
    user_serie.delete()
    messages.success(request, 'Serie removed from your collection.')
    return redirect('user_serie')



""" Movie """

@login_required
def user_movie_collection(request):
    user_movies = UserMovieCollection.objects.filter(user=request.user)
    available_movie = Movie.objects.all()
    status_filter = request.GET.get('status')
    if status_filter:
        user_movies = user_movies.filter(user_status=status_filter)
    return render(request, 'userCategory/user_movie.html', {
        'user_movie': user_movies,
        'available_movie': available_movie,
        })

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movie_details.html', {'movie': movie})

@login_required
def add_movie_to_collection(request, movie_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        movie = Movie.objects.get(api_id=movie_id)
        user_status = data.get('user_status')

        user_movie_collection, created = UserMovieCollection.objects.get_or_create(user=request.user, movie=movie)

        user_movie_collection.user_status = user_status
        if user_status in ['currently', 'pause']:
            user_movie_collection.current_episode = current_episode
        else:
            user_movie_collection.current_episode = None

        user_movie_collection.save()

        return JsonResponse({'success': True, 'message': 'Movie added to collection with user status: ' + user_status})

@login_required
def remove_movie_from_collection(request, movie_id):
    user_movie = get_object_or_404(UserMovieCollection, id=movie_id, user=request.user)
    user_movie.delete()
    messages.success(request, 'Movie removed from your collection.')
    return redirect('user_movie')


def most_popular_content(request):
    popular_manga = Manga.objects.order_by('-average_score').first()
    popular_anime = Anime.objects.order_by('-average_score').first()
    popular_serie = Serie.objects.order_by('-popularity').first()

    context = {
        'popular_manga': popular_manga,
        'popular_anime': popular_anime,
        'popular_serie': popular_serie,
    }
    return render(request, 'index.html', context)