from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from .models import Movie, Genre, Review
from rest_framework_simplejwt.tokens import RefreshToken


class MovieTestCase(APITestCase):
    
    def setUp(self):

        self.user = User.objects.create_user(username="testuser", password="Password@123")
        self.user.is_staff = True
        self.user.save()
        
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.genre = Genre.objects.create(name="Action")
        self.movie = Movie.objects.create(
            title="Test Movie", 
            overview="Test Overview", 
            poster_path="http://example.com", 
            release_date="2024-01-01",
            vote_average=8.5
        )
        self.movie.genres.add(self.genre)

    def test_movie_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_movie_create(self):
        data = {
            "title": "New Movie",
            "overview": "New Overview",
            "poster_path": "http://example.com",
            "release_date": "2024-02-01",
            "vote_average": 7.5,
            "genres": [{"id": self.genre.id}]
        }
        response = self.client.post(reverse('movie-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_movie_detail(self):
        response = self.client.get(reverse('movie-detail', args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_update(self):
        data = {
            "title": "Updated Movie",
            "overview": "Updated Overview",
            "poster_path": "http://example.com",
            "release_date": "2024-02-01",
            "vote_average": 7.5,
            "genres": [{"id": self.genre.id}]
        }
        response = self.client.put(reverse('movie-detail', args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_delete(self):
        response = self.client.delete(reverse('movie-detail', args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        




class GenreTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Password@123")
        self.user.is_staff = True
        self.user.save()
        
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.genre = Genre.objects.create(name="Action")

    def test_genre_list(self):
        response = self.client.get(reverse('genre-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_genre_create(self):
        data = {
            "name": "Comedy"
        }
        response = self.client.post(reverse('genre-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_genre_detail(self):
        response = self.client.get(reverse('genre-detail', args=(self.genre.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_genre_update(self):
        data = {
            "name": "Updated Action"
        }
        response = self.client.put(reverse('genre-detail', args=(self.genre.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_genre_delete(self):
        response = self.client.delete(reverse('genre-detail', args=(self.genre.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        




class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="Password@123")
        self.user.save()

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.genre = Genre.objects.create(name="Action")
        self.movie = Movie.objects.create(title="Test Movie", overview="Test Overview", 
                                          poster_path="http://example.com", release_date="2024-01-01",
                                          vote_average=8.5)
        self.movie.genres.add(self.genre)
        
        #self.review = Review.objects.create(user=self.user, rating=5, description="Great Movie", movie=self.movie)

    def test_review_create(self):
        data = {
            "rating": 4,
            "description": "Good Movie"
        }
        response = self.client.post(reverse('review-create', args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_review_create_duplicate(self):
        self.review = Review.objects.create(user=self.user, rating=5, description="Great Movie", movie=self.movie)
        
        data = {
            "rating": 5,
            "description": "Awesome Movie",
        }
        response = self.client.post(reverse('review-create', args=(self.movie.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.movie.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_detail(self):
        self.review = Review.objects.create(user=self.user, rating=5, description="Great Movie", movie=self.movie)
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_update(self):
        self.review = Review.objects.create(user=self.user, rating=5, description="Great Movie", movie=self.movie)
        data = {
            "rating": 3,
            "description": "Okay Movie",
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_review_delete(self):
        self.review = Review.objects.create(user=self.user, rating=5, description="Great Movie", movie=self.movie)
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_reviews(self):
        response = self.client.get(reverse('user-reviews'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        


class MovieByGenreTestCase(APITestCase):
    def setUp(self):
        
        self.genre1 = Genre.objects.create(name="Action")
        self.genre2 = Genre.objects.create(name="Drama")
        
        self.movie1 = Movie.objects.create(title="Action Movie", overview="Test Overview 1", 
                                           poster_path="http://example.com/1", release_date="2024-01-01",
                                           vote_average=9.0)
        self.movie2 = Movie.objects.create(title="Drama Movie", overview="Test Overview 2", 
                                           poster_path="http://example.com/2", release_date="2024-02-01",
                                           vote_average=8.0)
        self.movie3 = Movie.objects.create(title="Another Action Movie", overview="Test Overview 3", 
                                           poster_path="http://example.com/3", release_date="2024-03-01",
                                           vote_average=7.5)
        
        self.movie1.genres.add(self.genre1)
        self.movie2.genres.add(self.genre2)
        self.movie3.genres.add(self.genre1)
    
    def test_movies_by_genre_view(self):
        # Belirli bir genre'ye ait filmleri listeleyen endpoint'i test et
        url = reverse('movies-by-genre', args=[self.genre1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # İki film bu genre'ye ait
        self.assertEqual(response.data[0]['title'], self.movie1.title)
        self.assertEqual(response.data[1]['title'], self.movie3.title)
        
        # Başka bir genre için test et
        url = reverse('movies-by-genre', args=[self.genre2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Bir film bu genre'ye ait
        self.assertEqual(response.data[0]['title'], self.movie2.title)