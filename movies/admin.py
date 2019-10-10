from django.contrib import admin
from movies.models import Comment
from movies.models import Movie


admin.site.register(Movie)
admin.site.register(Comment)
