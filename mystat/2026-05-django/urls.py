from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from school import api, views

router = DefaultRouter()
router.register("characters", api.CharacterViewSet)
router.register("history", api.BattleViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.hello, name="hello"),
    path("weekday/", views.weekday, name="weekday"),
    path("quote/", views.quote, name="quote"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("projects/", views.projects, name="projects"),
    path("projects/<int:pk>", views.project, name="project"),
    path("contacts/", views.contacts, name="contacts"),
    path("schedule/", views.schedule_home, name="schedule-home"),
    path("schedule/week/", views.schedule_week, name="schedule-week"),
    path("schedule/teachers/", views.teachers, name="teachers"),
    path("schedule/lesson/<int:pk>/", views.lesson, name="lesson"),
    path("schedule/<str:day>/", views.schedule_day, name="schedule-day"),
    path("api/battle/", api.battle, name="battle"),
    path("api/", include(router.urls)),
    path("library/", include("school.library_urls")),
]
