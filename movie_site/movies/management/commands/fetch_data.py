from django.core.management.base import BaseCommand
from movies.utils import fetch_genres, fetch_popular_movies, save_genres, save_movie_details

class Command(BaseCommand):
    help = 'Fetch and save genres and popular movies from TMDB'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Fetching genres...'))
        genres_data = fetch_genres()
        if genres_data:
            save_genres(genres_data)
            self.stdout.write(self.style.SUCCESS('Successfully saved genres'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch genres'))

        self.stdout.write(self.style.SUCCESS('Fetching popular movies...'))
        movies_data = fetch_popular_movies()
        if movies_data:
            for movie_data in movies_data:
                save_movie_details(movie_data)
            self.stdout.write(self.style.SUCCESS('Successfully saved popular movies'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch popular movies'))