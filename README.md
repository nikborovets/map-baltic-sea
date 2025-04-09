
```bash
apt-get update
apt-get install certbot
certbot certonly --standalone -d map.nikborovets.ru
```


```bash
sudo apt update
sudo apt install fail2ban -y
```
```bash
#!/bin/bash

cat >/etc/fail2ban/filter.d/nginx-custom-block.conf <<'EOF'
[Definition]
failregex = ^<HOST> - - \[.*?\] "(?!GET /($|processed_graphs/|health)).*"
ignoreregex =
EOF

cat >>/etc/fail2ban/jail.local <<'EOF'

[nginx-custom-block]
enabled = true
port    = http,https
filter  = nginx-custom-block
logpath = /var/log/nginx/access.log
maxretry = 1
findtime = 60
bantime = 3600
action = iptables-multiport[name=nginx-custom-block, port="http,https"]
EOF

systemctl restart fail2ban
fail2ban-client status nginx-custom-block

```

`/var/log/nginx/access.log`

```bash
docker-compose up -d --build
docker-compose down
```