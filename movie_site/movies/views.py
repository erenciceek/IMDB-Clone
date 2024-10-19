from rest_framework import generics
from .models import Movie, Genre, Review
from .serializers import MovieSerializer, GenreSerializer, ReviewSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from .permissions import IsReviewUserOrReadOnly, IsAdminOrReadOnly
from .filters import MovieFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'overview', 'genres__name']
    ordering_fields = ['release_date', 'vote_average']
    
    
class MovieCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = MovieSerializer
    
    def perform_create(self, serializer):
        movie = serializer.save()
        genres_data = self.request.data.get('genres', [])
        genre_ids = [genre['id'] for genre in genres_data if 'id' in genre]
        genres = Genre.objects.filter(id__in=genre_ids)
        if len(genres) != len(genre_ids):
            missing_ids = set(genre_ids) - set(genres.values_list('id', flat=True))
            raise ValidationError(f"Invalid genre IDs: {missing_ids}")
        movie.genres.set(genres)



class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = MovieSerializer
    
    
    def perform_update(self, serializer):
        movie = serializer.save()
        genres_data = self.request.data.get('genres', [])
        genre_ids = [genre['id'] for genre in genres_data if 'id' in genre]
        genres = Genre.objects.filter(id__in=genre_ids)
        if len(genres) != len(genre_ids):
            missing_ids = set(genre_ids) - set(genres.values_list('id', flat=True))
            raise ValidationError(f"Invalid genre IDs: {missing_ids}")
        movie.genres.set(genres)



class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer

class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer



class ReviewListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rating', 'date']
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(movie__id=pk)


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        movie = Movie.objects.get(pk=pk)
       
        review_user = self.request.user
        review_queryset = Review.objects.filter(movie=movie ,user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")
        
        serializer.save(movie=movie, user=review_user) 


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    permission_classes = [IsReviewUserOrReadOnly]
    serializer_class = ReviewSerializer
    
    
    
class UserReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rating', 'date']
    
    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)
    
    
class MoviesByGenreView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        genre_id = self.kwargs.get('pk')
        return Movie.objects.filter(genres__id=genre_id)