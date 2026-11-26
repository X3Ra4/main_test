from random import choice

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import localdate

from .models import DAYS, Lesson, Teacher

PORTFOLIO = [
    {"id": 1, "name": "Книжкова полиця", "year": 2026, "state": "Прототип",
     "summary": "Каталог книжок та власні списки читання.", "body": "Expo Router, Open Library API, AsyncStorage."},
    {"id": 2, "name": "Розклад занять", "year": 2026, "state": "Готово",
     "summary": "Розклад для студентської групи.", "body": "Django, SQLite та окремі маршрути днів і занять."},
]


def hello(request):
    return HttpResponse("Hello, World!")


def weekday(request):
    return HttpResponse(DAYS[localdate().weekday()][1])


def quote(request):
    return HttpResponse(choice(["Починай з малого.", "Спостереження відкриває нові запитання.", "Практика додає впевненості."]))


def page(request, **context):
    return render(request, "school/page.html", context)


def portfolio(request):
    return page(request, title="Олег Огієнко", intro="Розробляю вебзастосунки та навчаю Python.",
                skills=[("Python", "advanced"), ("Django", "advanced"), ("React Native", "intermediate"), ("Solidity", "beginner")])


def projects(request):
    return page(request, title="Проєкти", projects=PORTFOLIO)


def project(request, pk):
    item = next((item for item in PORTFOLIO if item["id"] == pk), None)
    if item is None:
        raise Http404("Проєкт не знайдено")
    return page(request, title=item["name"], intro=item["summary"], detail=item["body"])


def contacts(request):
    return page(request, title="Контакти", contact="https://github.com/X3Ra4")


def schedule_home(request):
    label = f"Тиждень №{localdate().isocalendar().week}"
    return page(request, title="Розклад групи P35", intro=label, days=DAYS)


def schedule_week(request):
    all_lessons = list(Lesson.objects.select_related("teacher"))
    week = [(label, [lesson for lesson in all_lessons if lesson.day == slug]) for slug, label in DAYS]
    return page(request, title="Розклад на тиждень", week=week)


def schedule_day(request, day):
    label = dict(DAYS).get(day)
    if label is None:
        raise Http404("Некоректний день тижня")
    return page(request, title=label, week=[(label, Lesson.objects.filter(day=day).select_related("teacher"))])


def lesson(request, pk):
    item = get_object_or_404(Lesson.objects.select_related("teacher"), pk=pk)
    return page(request, title=item.subject, lesson=item)


def teachers(request):
    values = [{"name": teacher.name, "subjects": sorted({lesson.subject for lesson in teacher.lessons.all()}),
               "count": len(teacher.lessons.all())}
              for teacher in Teacher.objects.order_by("name").prefetch_related("lessons")]
    return page(request, title="Викладачі", teachers=values)
