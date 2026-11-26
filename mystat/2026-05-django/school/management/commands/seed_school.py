from datetime import time

from django.core.management.base import BaseCommand

from school.models import Book, Character, Lesson, Review, Teacher


class Command(BaseCommand):
    help = "Заповнює локальну БД демонстраційними даними"

    def handle(self, *args, **options):
        first, _ = Teacher.objects.get_or_create(name="Марія Сова")
        second, _ = Teacher.objects.get_or_create(name="Іван Лісовий")
        for teacher, subject, day, hour, room, cancelled in [
            (first, "Python", "monday", 9, "102", False),
            (second, "Бази даних", "monday", 11, "205", True),
            (second, "Веброзробка", "wednesday", 10, "306", False),
        ]:
            Lesson.objects.get_or_create(subject=subject, day=day, starts_at=time(hour), teacher=teacher,
                                         defaults={"room": room, "notes": "Зошит або ноутбук", "is_cancelled": cancelled})
        for name, hp, attack, defense in [("Knight", 100, 20, 5), ("Orc", 80, 15, 5)]:
            Character.objects.get_or_create(name=name, defaults={"hp": hp, "attack": attack, "defense": defense})
        book, _ = Book.objects.get_or_create(title="Місто", defaults={
            "author": "Валер’ян Підмогильний", "genre": "Роман", "summary": "Роман про життя у великому місті."})
        Review.objects.get_or_create(book=book, reader="Олена", defaults={"score": 5, "text": "Цікавий образ міста."})
        self.stdout.write(self.style.SUCCESS("Демо-дані створено."))
