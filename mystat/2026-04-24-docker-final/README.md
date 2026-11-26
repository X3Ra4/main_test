# Нотатки у Docker

Окремий образ вебінтерфейсу Nginx і окремий образ Python API, які піднімаються в мережі Compose. API доступний вебконтейнеру за DNS-іменем `api`. З хоста відкритий порт 8085.

```bash
docker compose up --build -d
docker compose ps
curl -f http://127.0.0.1:8085/api/notes
```

Інтерфейс: http://localhost:8085. Зупинка: `docker compose down`.
