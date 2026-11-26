# Telegram-бот на AWS EC2
Бот відповідає на `/start` та текстові повідомлення через long polling. Для Ubuntu на EC2 клонувати репозиторій у `/opt/mystat`, використовуючи доступ до цього репозиторію. Записати `TELEGRAM_BOT_TOKEN=...` у `/etc/mystat/telegram.env` з правами 600. Потім встановити `telegram.service` у `/etc/systemd/system/` та виконати:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now telegram
sudo systemctl status telegram
sudo journalctl -u telegram -n 25
```
Перевірка на реальному EC2 потребує Learner Lab та токена бота.
