from django.core.management.base import BaseCommand
from myapp.models import Anime
from datetime import date
import requests

class Command(BaseCommand):
    help = "Synchronise les animes depuis l'API et les stocke en BDD"

    def handle(self, *args, **options):
        url = "https://graphql.anilist.co"
        page = 1
        has_more = True

        while has_more:
            query = """
            query ($page: Int) {
                Page(page: $page, perPage: 50) {
                    media(type: ANIME) {
                        id
                        title {
                            romaji
                            english
                            native
                        }
                        coverImage {
                            large
                        }
                        description
                        genres
                        episodes
                        status
                        startDate {
                            year
                            month
                            day
                        }
                        endDate {
                            year
                            month
                            day
                        }
                        averageScore
                    }
                }
            }
            """
            response = requests.post(url, json={'query': query, 'variables': {'page': page}})
            data = response.json()

            animes = data['data']['Page']['media']
            if not animes:
                has_more = False
            else:
                for anime_data in animes:
                    start_date = None
                    end_date = None

                    if anime_data['startDate']:
                        start_year = anime_data['startDate'].get('year')
                        start_month = anime_data['startDate'].get('month')
                        start_day = anime_data['startDate'].get('day')

                        if start_year is not None and start_month is not None and start_day is not None:
                            start_date = date(start_year, start_month, start_day)

                    if anime_data['endDate']:
                        end_year = anime_data['endDate'].get('year')
                        end_month = anime_data['endDate'].get('month')
                        end_day = anime_data['endDate'].get('day')

                        if end_year is not None and end_month is not None and end_day is not None:
                            end_date = date(end_year, end_month, end_day)

                    Anime.objects.update_or_create(
                        api_id=anime_data['id'],
                        defaults={
                            'title_romaji': anime_data['title']['romaji'],
                            'title_english': anime_data['title']['english'],
                            'title_native': anime_data['title']['native'],
                            'cover_image': anime_data['coverImage']['large'],
                            'description': anime_data['description'],
                            'genres': anime_data['genres'],
                            'episodes': anime_data.get('episodes'),
                            'status': anime_data['status'],
                            'start_date': start_date,
                            'end_date': end_date,
                            'average_score': anime_data['averageScore'],
                        }
                    )
                page += 1
            self.stdout.write(f"Page {page} synchronisée")
