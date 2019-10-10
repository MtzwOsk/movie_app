from django_filters import DateFromToRangeFilter
from django_filters import FilterSet
from movies.models import Movie


class CommentsDateFilter(FilterSet):
    date = DateFromToRangeFilter(required=True, lookup_expr='range', field_name='comments__created')

    class Meta:
        model = Movie
        fields = ['comments__created']
