from bots.crawler import * 
from AI.train import save_db_to_fs
from extensions import app, db

dates = ['20241026', '20241027', '20241101', '20241029', '20241028']

#Crawler_News(modes='date-specific', dates_to_visit=dates).fetch()

save_db_to_fs('news')