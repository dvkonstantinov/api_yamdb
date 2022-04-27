# from django.contrib.auth import get_user_model
from django.db import models

# User = get_user_model()


class Auth(models.Model):
    pass

# Добавил модель юзера ибо там какие то извращени по условию 
# и просто  User = get_user_model() не сработает
#!!!!!!Возможно я не прав
class User(models.Model):
    pass


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='titles')
    genre = models.ManyToManyField('Genre',
                                   through='TitleGenre',
                                   related_name='titles')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.title} {self.genre}'

    class Meta:
        ordering = ['-id']


class Review(models.Model):
    pass


class Comment(models.Model):
    pass