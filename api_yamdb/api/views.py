from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .models import  Auth, User, Category, Genre, Title, Review
from .serializers import  AuthSerializer, UserSerializer, CategorySerializer
from .serializers import GenreSerializer, TitleSerializer, ReviewSerializer


class AuthViewSet(viewsets.ModelViewSet):
    pass

# Так же не знаю по поводу юзера
class UserViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass