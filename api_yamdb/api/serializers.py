#from django.contrib.auth import get_user_model
import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from users.models import Category, Genre, Title, Review, TitleGenre, Comment, User


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class CategorySerializer(CategoryCreateUpdateSerializer):

    def to_representation(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug,
        }

    def to_internal_value(self, data):
        category_slug = data
        return get_object_or_404(Category, slug=category_slug)


class GenreCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class GenreSerializer(GenreCreateUpdateSerializer):

    def to_representation(self, obj):
        return {
            'name': obj.name,
            'slug': obj.slug,
        }

    def to_internal_value(self, data):
        category_slug = data
        return get_object_or_404(Genre, slug=category_slug)


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    genre = GenreSerializer(many=True, required=True)
    year = serializers.IntegerField(required=True)

    class Meta:
        fields = ['id', 'name', 'year', 'description',  'category', 'genre']
        model = Title
        extra_kwargs = {
            'year': {'required': True}
        }

    def validate_year(self, value):
        now_year = datetime.date.today().year
        if value > now_year:
            raise serializers.ValidationError(
                "Год не может быть больше текущего")
        return value

    def validate(self, data):
        required_fields = ['year', 'name', 'category', 'genre']
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(
                    f'Поле "{field}" обязательно для заполнения')
        return data

    def create(self, validated_data):

        category = validated_data.pop('category')
        genres = validated_data.pop('genre')
        instance = Title.objects.create(**validated_data, category=category)
        for genre in genres:
            TitleGenre.objects.create(title=instance, genre=genre)
        return instance

    def update(self, instance, validated_data, partial=False):
        genres = ''
        instance_id = instance.id
        if 'genre' in self.initial_data:
            genres = validated_data.pop('genre')
        Title.objects.filter(id=instance_id).update(**validated_data)
        instance.refresh_from_db()
        instance.genre.clear()
        for genre in genres:
            TitleGenre.objects.create(title=instance, genre=genre)
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    
    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value.lower() == "me":
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    class Meta:
        fields = ("username", "email")
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()