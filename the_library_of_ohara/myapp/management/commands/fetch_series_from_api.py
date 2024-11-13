from django.core.management.base import BaseCommand
from myapp.models import Serie
from datetime import datetime
import requests

class Command(BaseCommand):
    help = "Synchronise les series depuis l'API et les stocke en BDD"

    def handle(self, *args, **kwargs):
        api_key = 'a863027759d28f0abab4b6264f23607f'
        url = f'https://api.themoviedb.org/3/tv/popular?api_key={api_key}&language=fr-FR&page=1'
        page = 1
        has_more = True

        response = requests.get(url)
        data = response.json()

        while has_more:
            url = f'{url}?api_key={api_key}&language=fr-FR&page={page}'
            response = requests.get(url)
            data = response.json()

            series = data.get('results', [])
            if not series:
                has_more = False
            else:
                for serie_data in series:
                    release_date = None
                    if serie_data['first_air_date']:
                        release_date = datetime.strptime(serie_data['first_air_date'], '%Y-%m-%d').date()

                    Serie.objects.update_or_create(
                    api_id=serie_data['id'],
                    defaults={
                        'title': serie_data['name'],
                        'overview': serie_data.get('overview'),
                        'poster_path': f"https://image.tmdb.org/t/p/w500{serie_data.get('poster_path')}",
                        'backdrop_path': f"https://image.tmdb.org/t/p/w500{serie_data.get('backdrop_path')}",
                        'release_date': release_date,
                    }
                )
            self.stdout.write(f"Page {page} synchronisée avec succès")
            page += 1
