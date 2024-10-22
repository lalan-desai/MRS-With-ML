# Generated by Django 4.1.13 on 2024-07-16 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('imdbid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('genre', models.CharField(max_length=100)),
                ('director', models.CharField(max_length=100)),
                ('writer', models.CharField(max_length=100)),
                ('actors', models.CharField(max_length=200)),
                ('plot', models.TextField()),
                ('language', models.CharField(max_length=100)),
                ('poster', models.URLField()),
                ('imdbRating', models.FloatField()),
                ('imdbVotes', models.BigIntegerField()),
                ('type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('languages', models.CharField(max_length=100)),
                ('genres', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.content')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'content')},
            },
        ),
    ]
