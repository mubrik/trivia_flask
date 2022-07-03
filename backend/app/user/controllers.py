'''
  holds the controllers of user module
'''
from typing import List, Dict
from urllib import response
from flask import request, abort, jsonify, Blueprint, make_response
from flask_jwt_extended import set_access_cookies, create_access_token
from app import db, jwt_manager
# models
from .models import User

# define blueprint
user_bp = Blueprint('user', __name__)


@user_bp.route('/users/signup', methods=['POST'])
def signup():
  # get data
  data = request.get_json()
  if not data:
    # empty abort
    abort(422, "Invalid request. Please provide a valid payload.")
  # check if user exists
  username: str|None = data.get('username')
  password: str|None = data.get('password')
  # check if username and password are provided
  if not username or not password:
    abort(422, "Invalid request. Please provide a valid username/password.")
    
  # check password length
  if len(password) < 6:
    abort(422, "Invalid request. Password must be at least 6 characters long.")
  
  # get user if exist
  user: User | None = User.query.filter(User.username == username).first()
  if user is not None:
    # user exists
    abort(401, "Username already exists.")
  # create user, password hashing done by flask_bcrypt setter
  new_user = User(username=username, password=password)
  try:
    return_user = new_user.insert().format()
    #  using cookies to store jwt
    # passing instance directly because user_identity_lookup callback function is registered
    access_token = create_access_token(identity=new_user)
    #  make response
    response = make_response(jsonify(return_user), 200)
    # set cookies
    set_access_cookies(response, access_token)
  except Exception as error:
    print(error)
    db.session.rollback()
    abort(503, "Error creating the user, try again later")
  finally:
    db.session.close()

  return response
  
@user_bp.route('/users/login', methods=['POST'])
def login():
  # get data
  data = request.get_json()
  if not data:
    # empty abort
    abort(422, "Invalid request. Please provide a valid payload.")
  # check if user exists
  username: str|None = data.get('username')
  password: str|None = data.get('password')
  # check if username and password are provided
  if not username or not password:
    abort(422, "Invalid request. Please provide a valid username/password.")
  # get user if exist
  user: User | None = User.query.filter(User.username == username).first()
  if user is None:
    # user exists
    abort(401, "User does not exist.")
  # check password
  if not user.verify_password(password):
    # password incorrect
    abort(401, "Password incorrect.")
  # user valid, create access token
  access_token = create_access_token(identity=user)
  #  make response
  response = make_response(jsonify(user.format()), 200)
  # set cookies
  set_access_cookies(response, access_token)
  return response
  
  
  
  

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