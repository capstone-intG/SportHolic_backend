from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.team import Team, Calendar
from models.users import User
from datetime import datetime 
from sqlalchemy import func, extract 

calendar_route = Blueprint('calendar_route', __name__)
@calendar_route.route("/api/calendar/planned_events", defaults={'match_date': None}, methods=['GET'])
@calendar_route.route("/api/calendar/planned_events/<match_date>", methods=['GET'])
@jwt_required()
def planned_events(match_date):
    userid = get_jwt_identity()
    user = User.query.filter_by(id=userid).first()
    if user is None:
        return jsonify({'msg': 'user not found'})

    team_name = user.team 

    team = Team.query.filter_by(team_name=team_name).first()

    if team is None:
        return jsonify({'msg': f'Team({team_name}) not found'}), 400

    if match_date is not None:
        year = match_date[:4]
        month = match_date[4:]
        try:
            match_date = datetime.strptime(match_date, "%Y%m")
        except ValueError:
            return jsonify({"msg": "date must be %Y%m (202411)"})
        if len(year) != 4 or len(month) != 2:
            return jsonify({"msg": "date must be %Y%m (202411)"})
        if match_date.year < datetime.now().year or match_date.month < datetime.now().month:
            return jsonify({"msg": "provide future dates from now"})

        matches = Calendar.query.filter(Calendar.is_past_game==False, Calendar.team_id==team.id, extract('year', Calendar.match_date)==year, extract("month", Calendar.match_date)==month).all() 
        if matches is None or len(matches) == 0:
            return jsonify({"msg": "no planned matches found"})
        return jsonify([match.to_dict_planned() for match in matches])
    
    matches = Calendar.query.filter_by(is_past_game=False, team_id=team.id).order_by(Calendar.match_date).all()

    if len(matches) == 0:
        return jsonify({'msg': 'no planned matches found'})
    else:
        res = {}
        for i, match in enumerate(matches):
            res[i] = match.to_dict_planned()
        return jsonify(res)

@calendar_route.route("/api/calendar/past_events", defaults={"match_date": None}, methods=['GET'])
@calendar_route.route("/api/calendar/past_events/<match_date>", methods=['GET'])
@jwt_required()
def past_events(match_date):
    userid = get_jwt_identity()
    user = User.query.filter_by(id=userid).first() 
    if user is None:
        return jsonify({"msg": "user not found"})
    
    team_name = user.team 
    team = Team.query.filter_by(team_name=team_name).first()

    if team is None:
        return jsonify({"msg": f"Team({team_name}) not found"})

    if match_date is not None: 
        year = match_date[:4]
        month = match_date[4:]
        try:
            match_date = datetime.strptime(match_date, "%Y%m")
        except ValueError:
            return jsonify({"msg": "date must be %Y%m (202411)"})
        if len(year) != 4 or len(month) != 2:
            return jsonify({"msg": "date must be %Y%m (202411)"})
        if match_date.year > datetime.now().year or match_date.month > datetime.now().month:
            return jsonify({"msg": "provide past dates from now"})

        matches = Calendar.query.filter(Calendar.is_past_game==True, Calendar.team_id==team.id, extract('year', Calendar.match_date)==year, extract("month", Calendar.match_date)==month).all() 
        if matches is None or len(matches) == 0:
            return jsonify({"msg": "no past matches found"})
        return jsonify([match.to_dict_past() for match in matches])

    matches = Calendar.query.filter_by(team_id=team.id, is_past_game=True).order_by(Calendar.match_date).all()

    if len(matches) == 0:
        return jsonify({"msg": "no past matches found"})
    else:
        res = {}
        for i, match in enumerate(matches):
            res[i] = match.to_dict_past()
        return jsonify(res)