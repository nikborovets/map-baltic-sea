
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
failregex = ^<HOST> - - \[.*?\] "(?!(?:GET /(?:\s|processed_graphs/|health\s)))[^"]+"
ignoreregex =
EOF

[Definition]
failregex = ^<HOST> - - \[.*?\] "(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) (/(?:.*\.(env|bak|old|dev|local|config|git|aws|ini|json|yml|yaml)|.*\.\.\/.*|.*\.git/config.*|.*composer\.lock.*|.*package-lock\.json.*|.*docker-compose.*|.*credentials.*|.*htaccess.*)) HTTP/1.[01]" (301|400|403|404|500|502|503|504)
            ^<HOST> - - \[.*?\] "(GET|POST|HEAD|PUT|DELETE|OPTIONS|PATCH) [^"]+" (400|403|404) .* "-" "((python-requests|curl|l9explore|dirbuster|nikto|Go-http-client|Wget|bot|scanner)[^"]*)"
            ^<HOST> - - \[.*?\] "(?!(?:GET /(?:\s|processed_graphs/|health\s)))[^"]+"
ignoreregex =


cat >>/etc/fail2ban/jail.local <<'EOF'

[nginx-custom-block]
enabled = true
port    = http,https
filter  = nginx-custom-block
logpath = /var/log/nginx/access.log
backend = polling
maxretry = 1
findtime = 60
bantime = 3600
action = iptables-multiport[name=nginx-custom-block, port="http,https"]
EOF

systemctl restart fail2ban
fail2ban-client status nginx-custom-block

sudo fail2ban-regex /var/log/nginx/access.log /etc/fail2ban/filter.d/nginx-custom-block.conf --print-all-matched
sudo fail2ban-client status nginx-custom-block
sudo iptables -L f2b-nginx-custom-block -n --line-numbers
```

```
/var/log/nginx/access.log
```

```bash
docker-compose up -d --build
docker-compose down
```