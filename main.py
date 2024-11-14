from extensions import app, admin_token
from flask_sqlalchemy import SQLAlchemy
from config import Config
from extensions import *
import logging
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime 

@jwt.token_in_blocklist_loader
def check_if_token_is_revoke(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in jwt_blocklist

#register all the routes 
from routes.login import login_route 
from routes.news import news_route 
from routes.calendar import calendar_route
from routes.stats import stats_route
from routes.predict import prediction_route
from routes.bots_routes import crawling_routes

app.register_blueprint(login_route)
app.register_blueprint(news_route)
app.register_blueprint(calendar_route)
app.register_blueprint(stats_route)
app.register_blueprint(prediction_route)
app.register_blueprint(crawling_routes)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def log_request_info():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    cur_time = datetime.now().strftime("%Y%m%d %H:%M")
    logger.info(f"{cur_time} Request from {client_ip} - Path: {request.path} - Method: {request.method}")

    
#docker network create my_net
#docker run -d --network my_net -p 5000:5000 -v C:\Users\user\Desktop\종설:/app my_app
#docker run -d --network my_net --name my_app_db -p 3308:3308 my_app_db
from bots.crawler import * 
if __name__ == '__main__':
    app.run(host='0.0.0.0')