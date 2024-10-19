from django.urls import path
from . import views 


urlpatterns = [
    path('movies/', views.MovieListView.as_view(), name='movie-list'),
    path('movies/<int:pk>/',views.MovieDetailView.as_view(), name='movie-detail'),
    path('movies/create/',views.MovieCreateView.as_view(), name='movie-create'),
    
    path('genres/', views.GenreListCreateView.as_view(), name='genre-list-create'),
    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),
    
    path('movies/<int:pk>/reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('movies/<int:pk>/reviews/create/', views.ReviewCreateView.as_view(), name='review-create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    
    path('user-reviews/', views.UserReviewsView.as_view(), name= 'user-reviews'),
    path('movies/genre/<int:pk>/', views.MoviesByGenreView.as_view(), name='movies-by-genre'),
]