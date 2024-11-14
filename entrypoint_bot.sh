#!/bin/sh

flask db init 

echo "[*] flask migration started"
flask db stamp head 
flask db migrate
flask db upgrade

echo "[*] init_db.py started"
python3 init_db.py

echo "[*] init_daemon.py started in background"
python3 init_daemon.py &

while true; do
  sleep 2  # 2초 대기
done