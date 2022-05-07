from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name='titles')
    genre = models.ManyToManyField('Genre',
                                   related_name='titles')
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message='Оценка не может быть ниже 1'
            ),
            MaxValueValidator(
                10, message='Оценка не может быть выше 10'
            ),
        ]
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'],
            name='unique_review',
        )]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    def __str__(self):
        return self.text
