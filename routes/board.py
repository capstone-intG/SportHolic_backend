from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.board import Board
from models.users import User
from extensions import db, app
from datetime import datetime 

board_routes = Blueprint('board_routes', __name__)

@board_routes.route("/api/board", defaults={'id': None}, methods=['GET'])
@board_routes.route("/api/board/<id>", methods=['GET'])
def board_get(id):
    if id is None:
        boards = Board.query.all()
        boards = [board.to_dict() for board in boards]

        return jsonify(boards)
    board = Board.query.filter_by(id=id).first()

    if board is not None:
        board = board.to_dict()
    else:
        board = {"msg": "no board post found"}

    return jsonify(board)


@board_routes.route("/api/board", methods=['POST'])
def board_post():
    rj = request.get_json()
    title, contents = rj['title'], rj['contents']
    now = datetime.now()

    if title is None:
        return jsonify({"msg": "provide title"})
    
    if contents is None:
        return jsonify({"msg": "provide contents"})

    with app.app_context():
        board = Board(title=title, contents=contents, written_date=now)
        db.session.add(board)
        db.session.commit()
        
        return jsonify({"msg": "post added to db", "board_id": board.id})
    
@board_routes.route("/api/board/<id>", methods=['PATCH'])
def board_patch(id):
    rj = request.get_json()
    title, contents = rj['title'], rj['contents']
    now = datetime.now()

    if title is None:
        return jsonify({"msg": "provide title"})
    
    if contents is None:
        return jsonify({"msg": "provide contents"})

    with app.app_context():
        board = Board.query.filter_by(id=id).first()
        board.contents=contents
        board.title=title 

        db.session.commit()
        return jsonify({"msg": "post updated"})

@board_routes.route("/api/board/<id>", methods=['DELETE'])
def board_delete(id):
    with app.app_context():
        board = Board.query.filter_by(id=id).first()
        db.session.delete(board)
        db.session.commit()
        return jsonify({"msg": "post deleted"})