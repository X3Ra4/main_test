# Два віртуальні хости Nginx

```bash
docker compose up -d
docker compose exec nginx nginx -t
curl -fsS -H 'Host: my.test.loc' http://127.0.0.1:8080/
curl -fsS -H 'Host: api.test.loc' http://127.0.0.1:8080/
docker compose down
```

Очікується окрема сторінка для кожного Host. Конфігурації та сторінки підключаються з хоста read-only.
