import datetime

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from users.models import Category, Genre, Title, TitleGenre, User
from reviews.models import Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    genre = GenreSerializer(many=True, required=True)
    rating = serializers.FloatField(
        source='reviews__score__avg',
        read_only=True
    )

    class Meta:
        fields = ['id', 'name', 'year', 'description', 'category', 'genre',
                  'rating']
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(many=True, slug_field='slug',
                             queryset=Genre.objects.all())
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())

    class Meta:
        fields = ['id', 'name', 'year', 'description', 'category', 'genre']
        model = Title

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
            genres = validated_data.pop('genre')
            instance = Title.objects.create(**validated_data)
            for genre in genres:
                TitleGenre.objects.create(title=instance, genre=genre)
            return instance


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
        model = Review

    def validate(self, data):
        if Review.objects.filter(
                title=self.context['view'].kwargs['title_id'],
                author=self.context['request'].user
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Нельзя оставлять больше 1 отзыва на произведение')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
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
