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
    pass


class Comment(models.Model):
    pass