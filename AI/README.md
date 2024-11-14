* train.py : contains Stat_Predictor and News_Predictor
    * News_Predictor class is used in classifier_func of Crawler_News to predict the categories of received news post.
    * Stat_Predictor class is used in /api/stat subroutes to predict the match result

Notes:
News_Predictor requires model.pt, however this file is too large to upload to github. 
Stat_Predictor requires stats_model.pkl, however this file is too large to upload to github.