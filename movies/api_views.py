from django.db.models import Count
from django.db.models import Window
from django.db.models.functions import RowNumber
from django_filters.rest_framework import DjangoFilterBackend
from movies.filters import CommentsDateFilter
from movies.models import Comment
from movies.models import Movie
from movies.serializers import CommentAddSerializer
from movies.serializers import CommentSerializer
from movies.serializers import MovieSerializer
from movies.serializers import MovieTitleSerializer
from movies.serializers import MovieTopRankSerializer
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from utils.omdb_api import get_data_from_omdb


class MovieViewset(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'id', 'imdb_rating']
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = MovieTitleSerializer(data=request.data)
        if serializer.is_valid():
            movie_obj = Movie.objects.filter(**serializer.validated_data).first()
            if movie_obj:
                serializer_movie = self.serializer_class(instance=movie_obj)
            else:
                data = get_data_from_omdb(**serializer.validated_data) if serializer.is_valid() else None
                if not data:
                    return self.get_message_error(**serializer.validated_data)
                data = {
                    Movie.imdb_mapper_to_model_field(k.lower()): v
                    for k, v in data.items() if v != 'N/A'  # exclude empty values
                }
                serializer_movie = self.serializer_class(data=data)
                if not serializer_movie.is_valid():
                    return self.get_message_error(**serializer.validated_data)
                self.perform_create(serializer_movie)
        headers = self.get_success_headers(serializer_movie.data)
        return Response(serializer_movie.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        self.serializer_class = MovieSerializer
        kwargs.update({'partial': True})
        return super().update(request, *args, **kwargs)

    @staticmethod
    def get_message_error(title):
        return Response({'error': 'Film {} doesnt exist in our records'.format(title)}, status=status.HTTP_200_OK)


class CommentViewset(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie__title', 'id']
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        self.serializer_class = CommentAddSerializer
        return super().create(request, *args, **kwargs)


class MovieRankViewset(ListModelMixin, GenericViewSet):
    serializer_class = MovieTopRankSerializer
    filterset_class = CommentsDateFilter
    http_method_names = ['get']
    queryset = Movie.objects.all()

    def retrieve(self, request, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        # here obtain proper count, first filtered by date
        return queryset.annotate(
            total_comments=Count('comments')
        ).annotate(
            rank=Window(expression=RowNumber())
        ).order_by('rank').values('id', 'rank', 'total_comments')
