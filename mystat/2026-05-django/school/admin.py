from django.contrib import admin

from .models import Battle, Book, Character, Lesson, Review, Teacher

for model in (Battle, Book, Character, Lesson, Review, Teacher):
    admin.site.register(model)
