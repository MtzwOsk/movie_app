from movies.models import Comment
from movies.models import Movie
from rest_framework import serializers


class MovieSerializer(serializers.ModelSerializer):
    released = serializers.DateField(format='%d %b %Y', input_formats=['%d %b %Y'], allow_null=True, required=False)

    class Meta:
        model = Movie
        exclude = ('created', 'modified')


class MovieSerializerID(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id',)


class MovieTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title',)


class CommentAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content', 'movie')

    def create(self, validated_data):
        return Comment.objects.create(**validated_data, movie=validated_data.pop('movie'))


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('content',)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data, movie=validated_data.pop('movie'))


class MovieTopRankSerializer(serializers.ModelSerializer):
    movie_id = serializers.ReadOnlyField(source='id')
    total_comments = serializers.SerializerMethodField(read_only=True)
    rank = serializers.SerializerMethodField(read_only=True)

    def get_total_comments(self, movie):
        return movie['total_comments']

    def get_rank(self, movie):
        return movie['rank']

    class Meta:
        model = Movie
        fields = ('movie_id', 'total_comments', 'rank')
