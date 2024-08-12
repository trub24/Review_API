from datetime import datetime
from django.core.validators import MaxValueValidator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from .constants import (
    NAME_MAX_LENGTH,
    SLUG_MAX_LENGTH,
    DESCRIPTION_MAX_LENGTH,
    VIEW_NAME_MAX_LENGTH,
    MIN_VALUE,
    MAX_VALUE
)


class CategoryAndGenreBaseClass(models.Model):
    name = models.CharField(
        'название',
        max_length=NAME_MAX_LENGTH,
        default=None
    )
    slug = models.SlugField(
        'slug',
        max_length=SLUG_MAX_LENGTH,
        unique=True
    )

    class Meta:
        ordering = ('name', )
        abstract = True

    def __str__(self):
        return self.name[:VIEW_NAME_MAX_LENGTH]


class ReviewAndCommentBaseClass(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(app_label)s_%(class)s_related'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date', )
        abstract = True

    def __str__(self):
        return self.text


class Category(CategoryAndGenreBaseClass):

    class Meta(CategoryAndGenreBaseClass.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryAndGenreBaseClass):

    class Meta(CategoryAndGenreBaseClass.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('название', max_length=NAME_MAX_LENGTH)
    year = models.SmallIntegerField(
        'год',
        validators=[MaxValueValidator(datetime.now().year)],
        db_index=True
    )
    description = models.TextField(
        'описание',
        max_length=DESCRIPTION_MAX_LENGTH,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        default=None,
        on_delete=models.SET_DEFAULT,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.name


class Review(ReviewAndCommentBaseClass):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(MIN_VALUE),
                    MaxValueValidator(MAX_VALUE)])

    class Meta(ReviewAndCommentBaseClass.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_relationships'
            ),
        ]


class Comment(ReviewAndCommentBaseClass):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta(ReviewAndCommentBaseClass.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
