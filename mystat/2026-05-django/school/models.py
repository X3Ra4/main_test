from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

DAYS = (
    ("monday", "Понеділок"), ("tuesday", "Вівторок"), ("wednesday", "Середа"),
    ("thursday", "Четвер"), ("friday", "П’ятниця"), ("saturday", "Субота"), ("sunday", "Неділя"),
)


class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name="lessons")
    subject = models.CharField(max_length=100)
    day = models.CharField(max_length=10, choices=DAYS)
    starts_at = models.TimeField()
    room = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        ordering = ("starts_at", "id")

    def __str__(self):
        return self.subject


class Character(models.Model):
    name = models.CharField(max_length=100)
    hp = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)])
    attack = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    defense = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Battle(models.Model):
    occurred_at = models.DateTimeField(auto_now_add=True)
    first = models.CharField(max_length=100)
    second = models.CharField(max_length=100)
    winner = models.CharField(max_length=100)
    rounds = models.PositiveIntegerField()


class Book(models.Model):
    title = models.CharField(max_length=160)
    author = models.CharField(max_length=120)
    genre = models.CharField(max_length=60)
    summary = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    reader = models.CharField(max_length=100)
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()

    def __str__(self):
        return f"{self.book} · {self.reader}"
