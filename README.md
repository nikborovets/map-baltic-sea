
```bash
apt-get update
apt-get install certbot
certbot certonly --standalone -d map.nikborovets.ru
```


```bash
sudo apt update
sudo apt install fail2ban -y
```

Конфиги
```bash
<!-- а тут action -->
/etc/fail2ban/action.d/iptables.conf

<!-- тут jailы -->
/etc/fail2ban/jail.local - может переопределять .conf
/etc/fail2ban/jail.conf

<!-- тут фильтры -->
/etc/fail2ban/filter.d/nginx-custom-block.conf
```

```bash
#!/bin/bash

cat >/etc/fail2ban/filter.d/nginx-custom-block.conf <<'EOF'
[Definition]
failregex = ^<HOST> - - \[.*?\] "(?!(?:GET /(?:\s|processed_graphs/|health\s)))[^"]+"
ignoreregex =
EOF

[Definition]
failregex = ^<HOST> - - \[.*?\] "(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) (/(?:.*\.(env|bak|old|dev|local|config|git|aws|ini|json|yml|yaml)|.*\.\.\/.*|.*\.git/config.*|.*composer\.lock.*|.*package-lock\.json.*|.*docker-compose.*|.*credentials.*|.*htaccess.*)) HTTP/1.[01]" (301|400|403|404|500|502|503|504)
            ^<HOST> - - \[.*?\] "(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) [^"]+" (400|403|404) .* "-" "((python-requests|curl|l9explore|dirbuster|nikto|Go-http-client|Wget|bot|scanner)[^"]*)"
            ^<HOST> - - \[.*?\] "(?!(?:GET /(?:\s|processed_graphs/|health\s)))[^"]+"
ignoreregex =


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

sudo fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/nginx-custom-block.conf --print-all-matched
sudo fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf

systemctl restart fail2ban

sudo fail2ban-client status sshd
sudo fail2ban-client status nginx-custom-block

sudo iptables -L f2b-nginx-custom-block -n -v --line-numbers
sudo iptables -L DOCKER-USER -n -v --line-numbers
```


Логи
```
sudo tail -f /var/log/fail2ban.log

sudo tail -f /var/log/nginx/access.log

sudo tail -f /var/log/auth.log
```

```bash
docker-compose up -d --build
docker-compose down
```