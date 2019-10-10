from django_filters import DateFromToRangeFilter
from django_filters import FilterSet
from movies.models import Movie


class CommentsDateFilter(FilterSet):
    date = DateFromToRangeFilter(required=True, lookup_expr='range', field_name='comments__created',
                                 error_messages={'required': 'Required date_after and date_before filters'})

    class Meta:
        model = Movie
        fields = ['comments__created']
