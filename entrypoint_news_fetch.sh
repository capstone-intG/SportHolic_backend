#!/bin/sh
echo "[*] flask migration started"
flask db stamp head 
flask db migrate
flask db upgrade


python3 news_fetch.py