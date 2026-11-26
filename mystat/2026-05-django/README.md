# Django: портфоліо, розклад, API боїв і бібліотека

Потрібен Python 3.12+. Встановіть залежності через `python -m pip install -r requirements.txt`, потім виконайте `python manage.py migrate`, `python manage.py seed_school` та `python manage.py runserver`.

| Завдання | Маршрути |
|---|---|
| Вступ до Django | `/`, `/weekday/`, `/quote/` |
| Портфоліо | `/portfolio/`, `/projects/`, `/contacts/` |
| Деталі за параметром | `/projects/1`, `/projects/2` |
| Розклад | `/schedule/`, `/schedule/week/`, `/schedule/monday/`, `/schedule/teachers/` |
| REST API | `/api/characters/`, `POST /api/battle/`, `/api/history/` |
| Фінальний проєкт | `/library/` та `/library/reviews/` |

Запит для бою: `{"character_1": 1, "character_2": 2}` після заповнення демонстраційних даних. CRUD каталогу й відгуків доступний через HTML-форми; для книжок є пошук, фільтр за жанром і сортування за назвою. Для адміністратора створіть користувача через `python manage.py createsuperuser`.

`python manage.py check` перевіряє конфігурацію, `python manage.py test` запускає перевірки маршрутів і CRUD.
