'''
  holds the controllers of user module
'''
from typing import List, Dict
from flask import request, abort, jsonify, Blueprint
from app import db
# models
from .models import User

# define blueprint
user_bp = Blueprint('user', __name__)


@user_bp.route('/users/<username>')
def get_user(username):

  if not username:
    # empty abort
    abort(422, "Username cant be empty string")

  # get user if exist
  user: User | None = User.query.filter(User.username == username).first()

  if user is None:
    abort(404, "User does not Exist")

  return jsonify({
    "success": True,
    "user": user.format()
  })


@user_bp.route('/users', methods=['POST'])
def create_user():
  username = request.get_json()['username']

  if not username:
    # empty abort
    abort(422, "Username cant be empty string")

  # get user if exist
  user: User | None = User.query.filter(User.username == username).first()

  if user is not None:
    # exists
    return jsonify({
      "success": True,
      "user": user.format()
    })

  # doesnt exist create
  new_user = User(username)
  try:
    return_user = new_user.insert().format()
  except Exception as error:
    print(error)
    db.session.rollback()
    abort(503, "Error creating that user")
  finally:
    db.session.close()

  return jsonify({
    "success": True,
    "user": return_user
  }), 201


@user_bp.route('/users/<int:user_id>/score', methods=['POST'])
def add_user_score(user_id):
  score = request.get_json()['score']

  # get user if exist
  user: User | None = User.query.get(user_id)

  if user is None:
    # error
    abort(404, "User does not exist")

  curr_score = [score for score in user.scores]
  curr_score.append(score)
  user.scores = curr_score
  try:
    return_user = user.update().format()
  except Exception as error:
    print(error)
    db.session.rollback()
    abort(503, "Error updating scores")
  finally:
    db.session.close()

  return jsonify({
    "success": True,
    "user": return_user
  })


# creating this mainly so my tests can all run smoothly with the same user
@user_bp.route('/users/<int:user_id>/delete', methods=['DELETE'])
def delete_user(user_id):
  # get user if exist
  user: User | None = User.query.get(user_id)

  if not user:
    # error
    abort(404, "User does not exist")

  try:
    user.delete()
  except Exception as error:
    print(error)
    db.session.rollback()
    abort(503, "Error deleting user")
  finally:
    db.session.close()

  return jsonify({
    "success": True,
    "id": user_id
  })
  
@user_bp.errorhandler(400)
def handle_400(error):
  # Bad Request
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Error in Query/Data",
      "error": 400
  }), 400


@user_bp.errorhandler(422)
def handle_422(error):
  # bad syntax
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Error in Query/Data",
      "error": 422
  }), 422


@user_bp.errorhandler(404)
def handle_404(error):
  # Not Found
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Resource not Found",
      "error": 404
  }), 404


@user_bp.errorhandler(405)
def handle_405(error):
  # Method Not Allowed
  return jsonify({
      "success": False,
      "message": "Method not allowed",
      "error": 405
  }), 405


@user_bp.errorhandler(503)
def handle_503(error):
  # Server cannot process the request
  return jsonify({
    "success": False,
    "message": "System Busy",
    "error": 503
  }), 503