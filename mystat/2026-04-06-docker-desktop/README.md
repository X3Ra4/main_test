# Docker Desktop
На Windows установлено Docker Desktop CLI. `docker --version` повернув `Docker version 29.7.2, build a7dcaa6`.

Перевірка рушія: `docker desktop status`, потім `docker version`. На момент перевірки клієнт доступний, але серверна частина Docker Desktop не запустилася в поточному сеансі. Для повної перевірки після запуску рушія виконати `docker run --rm hello-world`.
