# Щоденник настрою на AWS
Telegram-бот на EC2 з PostgreSQL на тому самому інстансі. Запис `/mood 8 прогулянка` зберігає оцінку та нотатку за поточний день, `/week` показує статистику. Дані ізольовані за Telegram user ID.

1. На Ubuntu EC2 клонувати публічний репозиторій у `/opt/mystat`. Встановити PostgreSQL та Python із пакетом venv. Команда: `sudo git clone https://github.com/X3Ra4/main_test.git /opt/mystat`.
2. Створити окрему роль і БД PostgreSQL для застосунку та виконати `schema.sql` під власником БД.
3. З директорії проєкту виконати `python3 -m venv .venv` і `.venv/bin/pip install -r requirements.txt`.
4. У `/etc/mystat/mood.env` записати `TELEGRAM_BOT_TOKEN=...` та `DATABASE_URL=...`. Зберігати файл із правами 600.
5. Скопіювати `mood.service` до `/etc/systemd/system/`, виконати `sudo systemctl daemon-reload` та `sudo systemctl enable --now mood`.
6. Перевірити /mood та /week з тестового Telegram-акаунта, статус `systemctl status mood` та логи `journalctl -u mood`.
