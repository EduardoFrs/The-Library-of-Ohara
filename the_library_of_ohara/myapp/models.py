from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Manga(models.Model):
    api_id = models.IntegerField(default=0)
    title_romaji = models.CharField(max_length=255)
    title_english = models.CharField(max_length=255, null=True, blank=True)
    title_native = models.CharField(max_length=255, null=True, blank=True)
    cover_image = models.URLField()
    description = models.TextField(null=True, blank=True)
    genres = models.JSONField(null=True, blank=True)
    chapters = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    average_score = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title_english or self.title_romaji

class UserMangaCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=20, choices=[
        ('Finished', 'Finished'),
        ('Currently Reading', 'Currently Reading'),
        ('Paused', 'Paused'),
        ('To Begin', 'To Begin'),
    ], default='To Begin')
    current_chapter = models.IntegerField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'manga')

    def __str__(self):
        return f"{self.user.username} - {self.manga.title_english or self.manga.title_romaji}"

class Anime(models.Model):
    api_id = models.IntegerField(default=0)
    title_romaji = models.CharField(max_length=255)
    title_english = models.CharField(max_length=255, null=True, blank=True)
    title_native = models.CharField(max_length=255, null=True, blank=True)
    cover_image = models.URLField()
    description = models.TextField(null=True, blank=True)
    genres = models.JSONField(null=True, blank=True)
    episodes = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    average_score = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title_english or self.title_romaji

class UserAnimeCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=20, choices=[
        ('Finished', 'Finished'),
        ('Currently Reading', 'Currently Reading'),
        ('Paused', 'Paused'),
        ('To Begin', 'To Begin'),
    ], default='To Begin')
    current_episode = models.IntegerField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')

    def __str__(self):
        return f"{self.user.username} - {self.anime.title_english or self.anime.title_romaji}"

class Serie(models.Model):
    api_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.URLField(null=True, blank=True)
    backdrop_path = models.URLField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class UserSerieCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=20, choices=[
        ('Finished', 'Finished'),
        ('Currently Watching', 'Currently Watching'),
        ('Paused', 'Paused'),
        ('To Begin', 'To Begin'),
    ], default='To Begin')
    current_episode = models.IntegerField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'serie')

    def __str__(self):
        return f"{self.user.username} - {self.serie.title}"

class Movie(models.Model):
    api_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.URLField(null=True, blank=True)
    backdrop_path = models.URLField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class UserMovieCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=20, choices=[
        ('Finished', 'Finished'),
        ('Currently Watching', 'Currently Watching'),
        ('Paused', 'Paused'),
        ('To Begin', 'To Begin'),
    ], default='To Begin')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"