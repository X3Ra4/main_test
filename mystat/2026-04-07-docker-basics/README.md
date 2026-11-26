# Інструменти в контейнері Ubuntu

```bash
docker build -t mystat-ubuntu-tools .
docker run -d --name mystat-ubuntu-tools mystat-ubuntu-tools
docker exec mystat-ubuntu-tools mc --version
docker exec mystat-ubuntu-tools htop --version
docker exec mystat-ubuntu-tools nano --version
docker exec -it mystat-ubuntu-tools bash
docker stop mystat-ubuntu-tools
```

У сесії bash можна запустити `mc`, `htop` та `nano` у терміналі.
