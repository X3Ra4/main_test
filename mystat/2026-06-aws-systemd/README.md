# Автозапуск на EC2
Для Ubuntu EC2 із Docker Engine та Compose клонувати репозиторій у `/opt/mystat`; потрібен доступ до приватного репозиторію. Встановити `mystat-notes.service` до `/etc/systemd/system/` та запустити:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now mystat-notes
sudo systemctl status mystat-notes
curl -f http://127.0.0.1:8085/api/notes
sudo systemctl restart mystat-notes
```
Вебконтейнер прив’язаний до loopback. Для перегляду з локального ПК використовуйте SSH-тунель `ssh -L 8085:127.0.0.1:8085 ubuntu@EC2_HOST`. Після перезапуску EC2 перевірити `systemctl is-enabled mystat-notes` та API ще раз.
