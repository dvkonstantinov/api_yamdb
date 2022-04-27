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
    pass


class Genre(models.Model):
    pass


class Title(models.Model):
    pass


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
    title_id = models.ForeignKey(
        Title, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    score = models.IntegerField()

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', 
        auto_now_add=True
    )
    review_id = models.ForeignKey(
        Review, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )

    def __str__(self):
        return self.text