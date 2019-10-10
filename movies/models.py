from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class MovieManger(models.Manager):
    def create_movie_from_omdbapi(self, **kwargs):
        pass


class Movie(TimeStampedModel):
    title = models.CharField(verbose_name=_('title'), max_length=255, db_index=True)
    released = models.DateField(verbose_name=_('released'), max_length=120, blank=True, null=True)
    imdb_id = models.CharField(verbose_name=_('imdb id'), max_length=30, blank=True)
    imdb_rating = models.DecimalField(verbose_name=_('imdb rating'), decimal_places=2, max_digits=4, null=True)
    country = models.CharField(verbose_name=_('country'), max_length=80, blank=True)
    director = models.CharField(verbose_name=_('director'), max_length=60, blank=True)

    class Meta:
        verbose_name = _('movie')
        verbose_name_plural = _('movies')
        # unique_together for title and released

    def __str__(self):
        return self.title

    _FIELD_MAPPER = {
            'imdbid': 'imdb_id',
            'imdbrating': 'imdb_rating'
        }

    @classmethod
    def imdb_mapper_to_model_field(cls, field_name):
        return cls._FIELD_MAPPER.get(field_name, field_name)


class Comment(TimeStampedModel):
    content = models.TextField(verbose_name=_('content'), max_length=500)
    movie = models.ForeignKey('Movie', related_name='comments', verbose_name=_('movie'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return '{} | {}'.format(self.movie.title, self.content[:20])
