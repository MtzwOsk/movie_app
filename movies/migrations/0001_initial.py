# Generated by Django 2.2.5 on 2019-10-10 07:44

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='title')),
                ('released', models.DateField(blank=True, max_length=120, null=True, verbose_name='released')),
                ('imdb_id', models.CharField(blank=True, max_length=30, verbose_name='imdb id')),
                ('imdb_rating', models.DecimalField(decimal_places=2, max_digits=4, null=True, verbose_name='imdb rating')),
                ('country', models.CharField(blank=True, max_length=80, verbose_name='country')),
                ('director', models.CharField(blank=True, max_length=60, verbose_name='director')),
            ],
            options={
                'verbose_name': 'movie',
                'verbose_name_plural': 'movies',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('content', models.TextField(max_length=500, verbose_name='content')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='movies.Movie', verbose_name='movie')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
        ),
    ]