from django.core.management.base import BaseCommand
from myapp.models import Movie
from datetime import datetime
import requests

class Command(BaseCommand):
    help = "Synchronise les films depuis l'API et les stocke en BDD"

    def handle(self, *args, **kwargs):
        api_key = 'a863027759d28f0abab4b6264f23607f'
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=fr-FR&page=1'
        page = 1
        has_more = True

        response = requests.get(url)
        data = response.json()

        while has_more:
            url = f'{url}?api_key={api_key}&language=fr-FR&page={page}'
            response = requests.get(url)
            data = response.json()

            movies = data.get('results', [])
            if not movies:
                has_more = False
            else:
                for movie_data in movies:
                    release_date = None
                    if movie_data.get('release_date'):
                        release_date = datetime.strptime(movie_data.get('release_date'), '%Y-%m-%d').date()

                    Movie.objects.update_or_create(
                    api_id=movie_data['id'],
                    defaults={
                        'title': movie_data.get('title'),
                        'overview': movie_data.get('overview'),
                        'poster_path': f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path')}",
                        'backdrop_path': f"https://image.tmdb.org/t/p/w500{movie_data.get('backdrop_path')}",
                        'release_date': release_date,
                    }
                )
            self.stdout.write(f"Page {page} synchronisée avec succès")
            page += 1