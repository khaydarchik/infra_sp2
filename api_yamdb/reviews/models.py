from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Введите имя категории.'
    )
    slug = models.SlugField(
        max_length=50,
        blank=True,
        unique=True,
        help_text='Введите slug категории.'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        help_text='Введите имя жанра.'
    )
    slug = models.SlugField(
        max_length=50,
        blank=True,
        unique=True,
        help_text='Введите slug жанра.'
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(help_text='Введите название произведения.')
    year = models.SmallIntegerField(
        help_text='Введите год выпуска произведения.',
        validators=[
            MaxValueValidator(3000),
            MinValueValidator(1)
        ]
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
        help_text='Добавьте описание произведению.'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        db_index=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        help_text='Выберите категорию произведения.'
    )
    genre = models.ManyToManyField(
        'Genre',
        through='Genre_Title',
        related_name='titles',
        help_text='Выберите жанр произведения.'
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    review = models.ForeignKey(
        'Review',
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Выберите отзыв для комментария.'
    )
    text = models.TextField(
        help_text='Текст комментария.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text[:50]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Выберите произведение для отзыва.'
    )
    text = models.TextField(
        help_text='Текст отзыва.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.SmallIntegerField(
        help_text='Оценка произведения.',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:50]


class Genre_Title(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre'
            )
        ]

    def __str__(self):
        return f'{self.title} / {self.genre}'
