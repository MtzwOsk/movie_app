from datetime import date
from unittest import mock

from django.urls import reverse
from movies.api_views import MovieRankViewset
from movies.models import Comment
from movies.models import Movie
from movies.serializers import CommentSerializer
from movies.serializers import MovieSerializer
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase


class MovieTest(APITestCase):

    def setUp(self):
        self.movie = Movie.objects.create(title='title1', released=date.today())

    def test_get_all_movies(self):
        Movie.objects.create(title='title2', released='2003-11-01')
        response = self.client.get(reverse('movies-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Movie.objects.count())

    def test_delete_movie(self):
        response = self.client.delete(reverse('movies-detail', kwargs={'pk': self.movie.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(0, Movie.objects.count())

    def test_update_movie(self):
        response = self.client.put(
            reverse('movies-detail', kwargs={'pk': self.movie.pk}), data={'released': '10 Dec 2019'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.get(id=self.movie.id).released.strftime('%d %b %Y'), response.data['released'])

    @mock.patch('movies.api_views.get_data_from_omdb', side_effect=lambda title: {'title': 'test'})
    def test_post_movie_save_from_external(self, mock_get):
        data = mock_get.side_effect('title')
        response = self.client.post(reverse('movies-list'), data=data)
        serializer = MovieSerializer(Movie.objects.get(**data))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(serializer.data, response.data)
        self.assertEqual(Movie.objects.get(**data).title, data.popitem()[1])

    def test_post_with_saved_movie(self):
        response = self.client.post(reverse('movies-list'), data={'title': self.movie.title})
        serializer = MovieSerializer(instance=self.movie)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(serializer.data, response.data)
        self.assertEqual(self.movie.title, response.data['title'])


class CommentTest(APITestCase):

    def test_post_comment(self):
        movie = Movie.objects.create(title='title')
        response = self.client.post(reverse('comments-list'), data={'movie': movie.pk, 'content': 'new_comment'})
        new_comment = Comment.objects.get(**response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['content'], new_comment.content)
        self.assertEqual(response.json()['movie'], movie.id)

    def test_post_comment_with_invalid_movie_id(self):
        response = self.client.post(reverse('comments-list'), data={'movie': Movie(id=1), 'content': 'new_comment'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_comments(self):
        movie = Movie.objects.create(title='title')
        comment_positive = Comment.objects.create(content='the grate movie 1', movie=movie)
        comment_negative = Comment.objects.create(content='the grate movie 2', movie=movie)
        response = self.client.get(reverse('comments-list'))
        serializer = CommentSerializer(Comment.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data[0]['content'], comment_positive.content)
        self.assertEqual(response.data[1]['content'], comment_negative.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RankMoviesByCommentTest(APITestCase):

    def test_get_rank_without_filter_date_range(self):
        movie_django = Movie.objects.create(title='django', released='2003-11-01')
        Comment.objects.create(content='the grate movie 1', movie=movie_django)
        response = self.client.get(reverse('rank-list'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_rank_with_date_range(self):
        add_date = date.today().strftime('%Y-%m-%d')
        facotry = APIRequestFactory()
        rank_view = MovieRankViewset.as_view({'get': 'list'})
        Movie.objects.create(title='kill bill', released='2003-10-03')
        movie_django = Movie.objects.create(title='django', released='2001-10-03')
        Comment.objects.create(content='the grate movie 1', movie=movie_django)
        request = facotry.get(reverse('rank-list'), data={'date_before': add_date, 'date_after': add_date})
        response = rank_view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, [{'movie_id': movie_django.id, 'rank': 1, 'total_comments': movie_django.comments.count()}]
        )
