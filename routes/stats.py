from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from Dict import STAT_FEATURES_DICT, STAT_FEATURES, STAT_FEATURES_KOR
from models.team import Team
from models.users import User 

stats_route = Blueprint('stats_route', __name__)

@stats_route.route("/api/stats", methods=['GET'])
@jwt_required()
def all_stats():
    userid = get_jwt_identity()
    user = User.query.filter_by(id=userid).first()
    if user is None:
        return jsonify({"msg": 'user not found'})
    
    team_name = user.team 

    team = Team.query.filter_by(team_name=team_name).first()
    if team is None:
        return jsonify({'msg': f'Team({team_name}) not found'})
    
    stats = team.stats
    res = [stat.to_dict() for stat in stats]
    return jsonify(res)

@stats_route.route("/api/stats/<int:round_num>", defaults={"feature_name": None}, methods=['GET'])
@stats_route.route("/api/stats/<int:round_num>/<feature_name>", methods=['GET'])
@jwt_required()
def round_stats(round_num, feature_name):
    userid = get_jwt_identity()
    user = User.query.filter_by(id=userid).first()
    if user is None:
        return jsonify({"msg": 'user not found'})
    
    team_name = user.team 
    team = Team.query.filter_by(team_name=team_name).first() 
    if team is None:
        return jsonify({'msg': f'Team({team_name}) not found'})

    stats = team.stats 

    if feature_name is not None: 
        for stat in stats:
            if stat.round_num==round_num: 
                stat_dict = stat.to_dict()
                if feature_name in stat_dict:
                    return jsonify({feature_name: stat_dict[feature_name]})
                else:
                    return jsonify({"msg": "feature name not exist"})

    for stat in stats:
        if stat.round_num==round_num: 
            return jsonify(stat.to_dict())
    return jsonify({"msg": "round_num not exist"})

@stats_route.route("/api/stats/graph", methods=['GET'])
@jwt_required()
def stats_graph():
    pass

@stats_route.route("/api/stats/feature_names", methods=['GET'])
def feature_names():
    lang = request.args.get("lang")

    if not lang:
        return jsonify({"msg": "/api/stats/feature_names?lang=? (en, kor)"})
    
    if lang == "en":
        return jsonify(STAT_FEATURES)
    else:
        return jsonify(STAT_FEATURES_KOR)


