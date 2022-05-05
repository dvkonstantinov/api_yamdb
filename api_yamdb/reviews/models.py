from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User, Title


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
    score = models.IntegerField(
        validators=[
            MinValueValidator(
                1, message='Поставь побольше'
            ),
            MaxValueValidator(
                10, message='Поставь поменьше'
            ),
        ]
    )

    def __str__(self):
        return self.text

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'],
            name='unique_review',
        )]


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
