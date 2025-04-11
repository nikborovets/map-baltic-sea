# Карта Балтийского моря

## Обзор проекта

Этот проект представляет собой веб-приложение для отображения карты Балтийского моря с использованием Flask в качестве бэкенда и Docker для контейнеризации. Приложение визуализирует данные из набора NetCDF-файлов, структурированных по различным географическим точкам Балтийского региона.

Проект связан с научной работой "Валидация массивов изменений уровня Балтийского моря из Baltic Sea Physics Reanalysis по данным наблюдений на береговых мареографах", представленной на конференции MARESEDU (Москва, Россия). [Открыть PDF](https://nikborovets.github.io/data/Borovets_theses_maresedu.pdf)

### Особенности
- Кэширование статических файлов и HTML-страниц для оптимизации производительности
- Обработка и отображение данных из файлов NetCDF
- Контейнеризация с использованием Docker
- Комплексные меры безопасности с помощью Fail2ban

## Настройка сервера

### Установка SSL-сертификата
```bash
apt-get update
apt-get install certbot
certbot certonly --standalone -d map.nikborovets.ru
```

### Установка Fail2ban для безопасности
```bash
sudo apt update
sudo apt install fail2ban -y
```

## Конфигурация безопасности

### Расположение конфигурационных файлов Fail2ban
```bash
# Файлы действий
/etc/fail2ban/action.d/iptables.conf

# Файлы jails
/etc/fail2ban/jail.local # может переопределять .conf
/etc/fail2ban/jail.conf

# Файлы фильтров
/etc/fail2ban/filter.d/nginx-custom-block.conf
```

### Настройка фильтров и правил Fail2ban

```bash
#!/bin/bash

# Создаем фильтр для блокировки подозрительных запросов
cat >/etc/fail2ban/filter.d/nginx-custom-block.conf <<'EOF'
[Definition]
failregex = ^<HOST> - - \[.*?\] "(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) (/(?:.*\.(env|bak|old|dev|local|config|git|aws|ini|json|yml|yaml)|.*\.\.\/.*|.*\.git/config.*|.*composer\.lock.*|.*package-lock\.json.*|.*docker-compose.*|.*credentials.*|.*htaccess.*)) HTTP/1.[01]" (301|400|403|404|500|502|503|504)
            ^<HOST> - - \[.*?\] "(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) [^"]+" (400|403|404) .* "-" "((python-requests|curl|l9explore|dirbuster|nikto|Go-http-client|Wget|bot|scanner)[^"]*)"
            ^<HOST> - - \[.*?\] "(?!(?:GET /(?:\s|processed_graphs/|health\s)))[^"]+"
ignoreregex =
EOF

# Добавляем наши правила в jail.local
cat >>/etc/fail2ban/jail.local <<'EOF'

[sshd]
enabled = true
port    = ssh
filter  = sshd[mode=aggressive]
backend = systemd
maxretry = 1
findtime = 300
bantime = 86400


[nginx-custom-block]
enabled = true
port    = http,https
filter  = nginx-custom-block
logpath = /var/log/nginx/access.log
backend = polling
maxretry = 1
findtime = 120
bantime = 86400
action = iptables-dockeruser

EOF

# Тестирование регулярных выражений
sudo fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/nginx-custom-block.conf --print-all-matched
sudo fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf

# Перезапускаем сервис
systemctl restart fail2ban

# Проверяем статус
sudo fail2ban-client status sshd
sudo fail2ban-client status nginx-custom-block

# Проверяем правила iptables
sudo iptables -L f2b-nginx-custom-block -n -v --line-numbers
sudo iptables -L DOCKER-USER -n -v --line-numbers
```

## Мониторинг логов

Проверка логов для отслеживания работы сервиса и попыток вторжения:

```bash
# Логи Fail2ban
sudo tail -f /var/log/fail2ban.log

# Логи доступа Nginx
sudo tail -f /var/log/nginx/access.log

# Логи аутентификации
sudo tail -f /var/log/auth.log
```

## Управление приложением

```bash
# Запустить приложение
docker-compose up -d --build

# Остановить приложение
docker-compose down
```