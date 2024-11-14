from extensions import admin_token
from config import Config 
import requests 
import time 
import os 
import hashlib
from bots.crawler import * 
from extensions import db, app
from models.news import Post 

"""
def set_admin_key():
    random_bytes = os.urandom(64)
    secret_key = hashlib.sha256(random_bytes).hexdigest()
    os.environ['ADMIN_KEY'] = secret_key
    return secret_key

secret_key = "66d4d27d0b49b1009c39a826b8ec88a7b0aabb5115dc843201e40c989216e8d4"
"""
def clean_db():
    with app.app_context():
        post_dates = Post.query.with_entities(Post.written_date).all() 
        db_dates_list = sorted(list(set([post_date.written_date.strftime("%Y%m%d") for post_date in post_dates])))
        min_date, max_date = datetime.strptime(db_dates_list[0], "%Y%m%d"), datetime.strptime(db_dates_list[-1], "%Y%m%d")
        if len(db_dates_list) > 7:
            Post.query.filter_by(written_date=min_date).delete()
            db.session.commit()
        

def news_daemon_func():
    while True:
        try:
            time.sleep(Config.DAEMON_news_refresh_time)
            Crawler_News(modes='today').fetch()
            clean_db()
            """
            headers = {'Authorization': secret_key}
            response = requests.get(f"http://220.88.39.23:{Config.SERVER_port}/crawling/fetch_today_news", headers=headers)
            """
        except Exception as e:
            print(f"[-] Error : {e}")

def calendar_daemon_func():
    while True:
        try: 
            time.sleep(Config.DAEMON_calendar_refresh_time)
            Crawler_Calendars(for_training=False).fetch()
            """
            headers = {'Authorization': secret_key}
            response = requests.get(f"http://220.88.39.23:{Config.SERVER_port}/crawling/fetch_calendar", headers=headers)
            """
        except Exception as e:
            print(f"[-] Error : {e}")

def stats_daemon_func():
    while True:
        try: 
            time.sleep(Config.DAEMON_stats_refresh_time)
            Crawler_Stats().fetch()
            """
            headers = {'Authorization': secret_key}
            response = requests.get(f"http://220.88.39.23:{Config.SERVER_port}/crawling/fetch_stats", headers=headers)
            """
        except Exception as e:
            print(f"[-] Error : {e}")

def players_daemon_func():
    while True:
        try: 
            time.sleep(Config.DAEMON_players_refresh_time)
            Crawler_Players().fetch()
            """
            headers = {'Authorization': secret_key}
            response = requests.get(f"http://220.88.39.23:{Config.SERVER_port}/crawling/fetch_players", headers=headers)
            """
        except Exception as e:
            print(f"[-] Error : {e}")