'''
  holds the controllers of trivia module
'''
from typing import List, Dict
from flask import request, abort, jsonify, Blueprint
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import func
from app import db
# models
from .models import Question, Category, Score

# questions pagination
QUESTIONS_PER_PAGE = 10

# define blueprint
trivia_bp = Blueprint('trivia', __name__)

# routes
@trivia_bp.route('/categories')
def get_all_categories():
  # get categories
  categories: List[Category] = Category.query.all()
  # return categories
  return jsonify(
    {
      "success": True,
      "categories": {category.id: category.type for category in categories} if categories else {},
      "total_categories": len(categories),
    }
  )


@trivia_bp.route('/questions')
def get_paginated_questions():
  # get page
  page = request.args.get('page', 1, type=int)
  # calculate start and end of items in a page
  end_item = page * QUESTIONS_PER_PAGE
  start_item = end_item - (QUESTIONS_PER_PAGE - 1)
  # query
  questions: List[Question] = Question.query\
      .filter(Question.id.between(start_item, end_item)).all()
  # all categories
  all_categories: List[Category] = Category.query.all()
  # return questions
  return jsonify(
    {
      "success": True,
      "questions": [question.format() for question in questions] if questions else [],
      "categories": {category.id: category.type for category in all_categories} if all_categories else {},
      "total_questions": len(questions),
      "current_category": 'Science',  # current of?
    }
  )


@trivia_bp.route('/questions', methods=['POST'])
def create_question():
  # vars
  key_set = {'question', 'answer', 'category', 'difficulty'}
  request_data = request.get_json()
  # confirm keys in data
  diff = key_set.difference(set(request_data.keys()))
  if len(diff) > 0:
    abort(422, 'Missing Fields: ' + str(diff))
  # make instance
  try:
    question_obj = Question(**request_data)
    question = question_obj.insert().format()
  except Exception as e:
    print(e)
    abort(400)
  finally:
    db.session.close()

  return jsonify({
    "success": True,
    "question": question,
  }), 201


@trivia_bp.route('/questions/<int:question_id>', methods=["DELETE"])
def delete_question(question_id: int):
  # get question
  question: Question | None = Question.query.get(question_id)

  if not question:
    abort(404, "Item not found")

  try:
    question.delete()
  except Exception as error:
    # change this to db error later
    print(error)
    abort(404)
  finally:
    db.session.close()

  return jsonify({
    "success": True,
    "id": question_id
  }), 200


@trivia_bp.route('/categories', methods=['POST'])
def create_category():
  # vars
  category_type: str | None = request.get_json()["type"]

  # confirm valid query
  if not category_type:
    # invalid query
    abort(422, "Empty Field in body: type")

  # confirm type doesnt exist
  catgry_check: Category | None = Category.query.filter(
      Category.type == category_type).first()
  if catgry_check is not None:
    abort(400, "That Category already exists")

  # create
  new_category = Category(category_type)
  # add
  try:
    new_cat = new_category.insert().format()
  except Exception as error:
    # db error most likely, not sure what to tell the user...
    db.session.rollback()
    print(error)
    abort(503, "System busy, Cant process request")
  finally:
    db.session.close()

  return jsonify({
    "success": True,
    "category": new_cat
  }), 201

# creating this mainly so my tests can all run smoothly with the same category


@trivia_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
  # get category if exist
  category: Category | None = Category.query.get(category_id)

  if not category:
    # error
    abort(404, "Category does not exist")

  try:
    category.delete()
  except Exception as error:
    print(error)
    db.session.rollback()
    abort(503, "Error deleting category")
  finally:
    db.session.close()

  return jsonify({"success": True})


@trivia_bp.route('/questions/search', methods=['POST'])
def search_questions():
  # get page
  search_term: str|None = request.get_json()["searchTerm"] 
  # checking for none only as empty string shouldn't error
  if search_term is None:
    abort(400, 'Invalid search query')

  if search_term == "":
    # empty string, return early
    return jsonify(
      {
        "success": True,
        "questions": [],
        "total_questions": 0,
        "current_category": "Placeholder"
      }
    )

  # seacrh db
  try:
    questions: List[Question] = Question.query.filter(
        Question.question.ilike(f'%{search_term}%')).all()
  except Exception as error:
    print(error)
    # most likely a db error
    abort(400, 'Invalid search query')

  return jsonify(
    {
      "success": True,
      "questions": [question.format() for question in questions],
      "total_questions": len(questions),
      "current_category": "Placeholder"
    }
  )


@trivia_bp.route('/categories/<int:category_id>/questions')
def get_questions_by_category(category_id):
  # check if categorey exist
  category: Category | None = Category.query.get(category_id)

  if not category:
    abort(400, 'Category does not exist')

  # query
  questions: List[Question] = Question.query.filter(
      Question.category == category_id).all()

  return jsonify(
    {
      "success": True,
      "questions": [question.format() for question in questions],
      "total_questions": len(questions)
    }
  )


@trivia_bp.route('/quizzes', methods=['POST'])
def get_play_next_question():
  request_data: Dict|None = request.get_json()
  
  if not request_data:
    abort(400, 'Invalid request')
  
  previous_questions: List|None = request_data['previous_questions']
  quiz_category_id: int|None = request_data['quiz_category']['id']

  if quiz_category_id is None:
    abort(422, "Quiz category missing")

  if quiz_category_id == 0:
    # user selected all, only filter id
    question:Question|None = Question.query.filter(~Question.id.in_(previous_questions))\
      .order_by(func.random()).limit(1).first()
  else:
    question:Question|None = Question.query.filter(Question.category == int(quiz_category_id))\
      .filter(~Question.id.in_(previous_questions)).order_by(func.random()).limit(1).first()


  return jsonify(
    {
      "success": True,
      "question": question.format() if question is not None else False,
    }
  )
  
@trivia_bp.route('/quizzes/savescore', methods=['POST'])
@jwt_required()
def save_scores():
  request_data: Dict|None = request.get_json()
  if not request_data:
    abort(400, 'Invalid request')
  score: int|None = request_data['score']
  questions: int|None = request_data['questions']
  if score is None:
    abort(400, 'Invalid request')
  user_id = current_user.id
  new_score = Score(user=user_id, score=score, questions=questions)
  try:
    new_score.insert()
  except Exception as error:
    print(error)
    abort(503, "System busy, Cant process request")
  finally:
    db.session.close()
  return jsonify(
    {
      "success": True,
      "score": score,
    }
  )
  
@trivia_bp.errorhandler(400)
def handle_400(error):
  # Bad Request
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Error in Query/Data",
      "error": 400
  }), 400


@trivia_bp.errorhandler(422)
def handle_422(error):
  # bad syntax
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Error in Query/Data",
      "error": 422
  }), 422


@trivia_bp.errorhandler(404)
def handle_404(error):
  # Not Found
  print(error.description)
  return jsonify({
      "success": False,
      "message": error.description if error.description is not None else "Resource not Found",
      "error": 404
  }), 404


@trivia_bp.errorhandler(405)
def handle_405(error):
  # Method Not Allowed
  return jsonify({
      "success": False,
      "message": "Method not allowed",
      "error": 405
  }), 405


@trivia_bp.errorhandler(503)
def handle_503(error):
  # Server cannot process the request
  return jsonify({
    "success": False,
    "message": "System Busy",
    "error": 503
  }), 503