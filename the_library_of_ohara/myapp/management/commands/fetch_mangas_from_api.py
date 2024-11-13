from django.core.management.base import BaseCommand
from myapp.models import Manga
from datetime import date
import requests

class Command(BaseCommand):
    help = "Synchronise les mangas depuis l'API et les stocke en BDD"

    def handle(self, *args, **options):
        url = "https://graphql.anilist.co"
        page = 1
        has_more = True

        while has_more:
            query = """
            query ($page: Int) {
                Page(page: $page, perPage: 50) {
                    media(type: MANGA) {
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
                        chapters
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

            mangas = data['data']['Page']['media']
            if not mangas:
                has_more = False
            else:
                for manga_data in mangas:
                    start_date = None
                    end_date = None

                    if manga_data['startDate']:
                        start_year = manga_data['startDate'].get('year')
                        start_month = manga_data['startDate'].get('month')
                        start_day = manga_data['startDate'].get('day')

                        if start_year is not None and start_month is not None and start_day is not None:
                            start_date = date(start_year, start_month, start_day)

                    if manga_data['endDate']:
                        end_year = manga_data['endDate'].get('year')
                        end_month = manga_data['endDate'].get('month')
                        end_day = manga_data['endDate'].get('day')

                        if end_year is not None and end_month is not None and end_day is not None:
                            end_date = date(end_year, end_month, end_day)

                    Manga.objects.update_or_create(
                        api_id=manga_data['id'],
                        defaults={
                            'title_romaji': manga_data['title']['romaji'],
                            'title_english': manga_data['title']['english'],
                            'title_native': manga_data['title']['native'],
                            'cover_image': manga_data['coverImage']['large'],
                            'description': manga_data['description'],
                            'genres': manga_data['genres'],
                            'chapters': manga_data.get('chapters'),
                            'status': manga_data['status'],
                            'start_date': start_date,
                            'end_date': end_date,
                            'average_score': manga_data['averageScore'],
                        }
                    )
                page += 1
            self.stdout.write(f"Page {page} synchronisée")
