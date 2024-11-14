These files use flask Blueprint() to define subroutes. In /main.py, those blueprints are imported and added to main route.

Files
* calendar.py : defines all routes for /api/calendar subroutes
* login.py : defines routes for /api/user 
    * current supported route is /api/user/token (responsible for getting tokens that will be used throughout the whole route)
* news.py : defines routes for /api/news subroutes
* predict.py : defines routes for /api/predict subroutes
* stats.py : defines routes fro /api/stats subroutes