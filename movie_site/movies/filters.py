import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    release_date = django_filters.DateFilter(field_name='release_date')
    release_date__gt = django_filters.DateFilter(field_name='release_date', lookup_expr='gt')
    release_date__lt = django_filters.DateFilter(field_name='release_date', lookup_expr='lt')
    vote_average__gt = django_filters.NumberFilter(field_name='vote_average', lookup_expr='gt')
    vote_average__lt = django_filters.NumberFilter(field_name='vote_average', lookup_expr='lt')
    genres = django_filters.CharFilter(field_name='genres__name', lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'vote_average', 'genres']