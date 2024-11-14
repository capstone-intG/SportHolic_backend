#!/bin/sh

echo "[*] flask migration started"
flask db stamp head
flask db migrate
flask db upgrade

gunicorn --reload -w 6 --forwarded-allow-ips='*' --worker-class gthread -b 0.0.0.0:5000 main:app