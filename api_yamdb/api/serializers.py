from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from users.models import User
from reviews.models import Category, Genre, Title, Review, Comment
from reviews.constants import (
    EMAIL_MAX_LENGTH,
    USERNAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
    NAME_MAX_LENGTH,
    ROLE_MAX_LENGTH
)
from .utils import encode_confirmation_code, send_email


class UserSingUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        regex=r'^[\w.@+-]+\Z',
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH,
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Не валидный никнейм')
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        try:
            user, created = User.objects.get_or_create(
                username=username,
                email=email,
            )
            user.confirmation_code = encode_confirmation_code(
                username=username,
                email=email
            )
            user.save()
            send_email(email=user.email, code=user.confirmation_code)
            return user
        except IntegrityError:
            if User.objects.filter(username=username):
                if User.objects.filter(email=email):
                    raise serializers.ValidationError({
                        field_name: ['Уже использется']
                        for field_name in self.fields
                    })
                raise serializers.ValidationError({
                    'username': ['Уже использется']
                })
            raise serializers.ValidationError({
                'email': ['Уже использется']
            })


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,)
    confirmation_code = serializers.CharField(required=True,)

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs['username'])
        if user.confirmation_code != attrs['confirmation_code']:
            raise serializers.ValidationError('Не верный код доступа')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_MAX_LENGTH,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=False
    )
    last_name = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=False
    )
    role = serializers.ChoiceField(
        choices=User.Role.choices,
        required=False,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Не валидный никнейм')
        return value


class EditUserSerializer(UserSerializer):
    role = serializers.CharField(max_length=ROLE_MAX_LENGTH, read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=NAME_MAX_LENGTH, required=True,)
    slug = serializers.SlugField(
        max_length=SLUG_MAX_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=NAME_MAX_LENGTH, required=True,)
    slug = serializers.SlugField(
        max_length=SLUG_MAX_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True
    )
    rating = serializers.IntegerField(
        default=None,
        read_only=True,
    )

    class Meta:
        model = Title
        fields = (
            'id', 'category', 'genre', 'name', 'year', 'rating', 'description'
        )

    def validate_genre(self, data):
        if not data:
            raise serializers.ValidationError('Необходимо указать жанр(ы).')
        return data

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True
    )
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(
        read_only=True,
        default=None
    )

    class Meta:
        model = Title
        fields = (
            'id', 'category', 'genre', 'name', 'year', 'rating', 'description'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            review = Review.objects.filter(
                title=self.context['view'].kwargs.get('title_id'),
                author=self.context['request'].user
            )
            if review.exists():
                raise serializers.ValidationError(
                    'Ваш отзыв на это произведение уже опубликован'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
