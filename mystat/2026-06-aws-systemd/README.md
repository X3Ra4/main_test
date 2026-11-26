# Автозапуск на EC2
Для Ubuntu EC2 із Docker Engine та Compose клонувати публічний репозиторій у `/opt/mystat`. Встановити `mystat-notes.service` до `/etc/systemd/system/` та запустити: Команда: `sudo install -d -o "$USER" /opt/mystat && git clone https://github.com/X3Ra4/main_test.git /opt/mystat`.
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now mystat-notes
sudo systemctl status mystat-notes
curl -f http://127.0.0.1:8085/api/notes
sudo systemctl restart mystat-notes
```
Вебконтейнер прив’язаний до loopback. Для перегляду з локального ПК використовуйте SSH-тунель `ssh -L 8085:127.0.0.1:8085 ubuntu@EC2_HOST`. Після перезапуску EC2 перевірити `systemctl is-enabled mystat-notes` та API ще раз.
