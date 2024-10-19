import requests
from .models import Movie, Genre

API_KEY = '485e567c18f1cf10622b8d24c79d78a3'
BASE_URL = 'https://api.themoviedb.org/3'
GENRES_URL = f'{BASE_URL}/genre/movie/list?language=en&api_key={API_KEY}'
POPULAR_MOVIES_URL = f'{BASE_URL}/movie/popular?language=en&api_key={API_KEY}'

def fetch_genres():
    response = requests.get(GENRES_URL)
    if response.status_code == 200:
        return response.json().get('genres', [])
    else:
        print(f"Failed to fetch genres: {response.status_code}, {response.text}")
    return []

# def fetch_popular_movies():
#     response = requests.get(POPULAR_MOVIES_URL)
#     if response.status_code == 200:
#         return response.json().get('results', [])
#     else:
#         print(f"Failed to fetch popular movies: {response.status_code}, {response.text}")
#     return []

def fetch_popular_movies(max_movies=100):
    all_movies = []
    page = 1
    while len(all_movies) < max_movies:
        response = requests.get(f"{POPULAR_MOVIES_URL}&page={page}")
        if response.status_code == 200:
            data = response.json()
            movies = data.get('results', [])
            all_movies.extend(movies)
            if page >= data.get('total_pages', 1):
                break
            page += 1
        else:
            print(f"Failed to fetch popular movies: {response.status_code}, {response.text}")
            break
    return all_movies[:max_movies]


def save_genres(genres_data):
    for genre_data in genres_data:
        Genre.objects.update_or_create(
            genre_id=genre_data['id'],
            defaults={'name': genre_data['name']}
        )

def save_movie_details(movie_data):
    movie, created = Movie.objects.update_or_create(
        tmdb_id=movie_data['id'], 
        defaults={
            'title': movie_data['title'],
            'overview': movie_data['overview'],
            'poster_path': f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}" if movie_data['poster_path'] else '',
            'release_date': movie_data['release_date'],
            'vote_average': movie_data['vote_average'],
        }
    )

    if 'genres' in movie_data:
        genre_ids = [genre['id'] for genre in movie_data['genres']]
    elif 'genre_ids' in movie_data:
        genre_ids = movie_data['genre_ids']
    else:
        genre_ids = []

    genres = Genre.objects.filter(genre_id__in=genre_ids)
    movie.genres.set(genres)