from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, filters, mixins, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdminOrReadOnlyPermission
from .models import Auth, User, Category, Genre, Title, Review
from .serializers import AuthSerializer, UserSerializer, CategorySerializer, \
    CategoryCreateUpdateSerializer, GenreCreateUpdateSerializer
from .serializers import GenreSerializer, TitleSerializer, ReviewSerializer


class AuthViewSet(viewsets.ModelViewSet):
    pass


# Так же не знаю по поводу юзера
class UserViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    # permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug',)
    lookup_field = 'slug'

    def get_serializer_class(self):
        if hasattr(self, 'action') and (self.action == 'create'
                                        or self.action == 'update'):
            return CategoryCreateUpdateSerializer
        return CategorySerializer


class GenreViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    # permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug',)
    lookup_field = 'slug'

    def get_serializer_class(self):
        if hasattr(self, 'action') and (self.action == 'create'
                                        or self.action == 'update'):
            return GenreCreateUpdateSerializer
        return GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    # permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_queryset(self):
        all_fields = {
            'genre__slug': self.request.query_params.get('genre'),
            'category__slug': self.request.query_params.get('category'),
            'name': self.request.query_params.get('name'),
            'year': self.request.query_params.get('year'),
        }
        filter_fields = {k: v for k, v in all_fields.items() if v is not None}
        queryset = Title.objects.filter(**filter_fields)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass