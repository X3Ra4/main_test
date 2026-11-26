import os

import psycopg

from telegram_api import poll


def add_entry(connection, user_id, score, note):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO mood_entries (user_id, day, score, note) VALUES (%s, CURRENT_DATE, %s, %s)
            ON CONFLICT (user_id, day) DO UPDATE SET score=EXCLUDED.score, note=EXCLUDED.note
            """, (user_id, score, note))


def report(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT count(*), round(avg(score), 1), min(score), max(score)
            FROM mood_entries WHERE user_id=%s AND day >= CURRENT_DATE - 6
            """, (user_id,))
        count, average, low, high = cursor.fetchone()
    if not count:
        return "За останні 7 днів записів ще немає."
    return f"За останні 7 днів: {count} записів, середнє {average}/10, мінімум {low}, максимум {high}."


def reply(message, connection):
    if message["chat"]["type"] != "private":
        return "Щоденник працює в приватному чаті."
    user_id = message["from"]["id"]
    command, *args = message["text"].strip().split(maxsplit=2)
    command = command.partition("@")[0]
    if command == "/mood":
        if not args or not args[0].isdigit() or len(args[0]) > 2 or not 1 <= int(args[0]) <= 10:
            return "Приклад запису: /mood 8 Прогулянка"
        note = args[1].strip() if len(args) > 1 else ""
        if len(note) > 500:
            return "Нотатка має містити щонайбільше 500 символів."
        add_entry(connection, user_id, int(args[0]), note)
        return "Запис за сьогодні збережено."
    if command == "/week":
        return report(connection, user_id)
    return "Команди: /mood 8 нотатка, /week — підсумок за 7 днів."


def handle(message):
    with psycopg.connect(os.environ["DATABASE_URL"], options="-c timezone=Europe/Kyiv") as connection:
        return reply(message, connection)


if __name__ == "__main__":
    poll(os.environ["TELEGRAM_BOT_TOKEN"], handle)
