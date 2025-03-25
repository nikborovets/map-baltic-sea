
```
apt-get update
apt-get install certbot
certbot certonly --standalone -d map.nikborovets.ru

docker-compose up -d --build
docker-compose down
```