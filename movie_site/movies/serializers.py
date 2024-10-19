from rest_framework import serializers
from .models import Movie, Genre, Review

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'genre_id']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'overview', 'poster_path', 'release_date', 'vote_average', 'genres']
    
    
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'movie', 'rating', 'description', 'date']
        read_only_fields = ['user', 'movie']
        
    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 1 and 10.")
        return value