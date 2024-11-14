# SportHolic_backend

Initial Booting
    * Run below commands on 3 different terminals
1. docker-compose -f docker-compose.db.yml up (runs db container)
2. docker-compose -f docker-compose.bot.yml up (runs bot crawler container)
3. docker-compose -f docker-compose.backend.yml up (runs backend container)
* ignore news_fetch.yml because it is used for fetching news contents for training AI 

Troubleshooting
* if having trouble with rev-id, edit in entrypoint_backend.sh "flask db stamp head - flask db migrate - flask db upgrade" --> "flask db revision --rev-id [random rev id] - flask db stamp head - flask db migrate -flask db upgrade"
* if having trouble with "no migration folder", add "flask db init" to the first line of entrypoint_backend.sh

Files
* init_db.py : runs inital crawlers (Crawler_News, Crawler_Calendar, Crawler_Stats, Crawler_Players)
* init_daemon.py : add daemon process and the daemon frequently fetches informations from different sites. (frequency is defined in /config.py)
* requirements.py : defines all the packages used in the project