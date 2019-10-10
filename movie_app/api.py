from movies import api_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'top', api_views.MovieRankViewset, base_name='rank')
router.register(r'movies', api_views.MovieViewset, base_name='movies')
router.register(r'comments', api_views.CommentViewset, base_name='comments')
