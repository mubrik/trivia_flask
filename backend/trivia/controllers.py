from typing import List, Dict
from flask import request, abort, jsonify
from sqlalchemy import func

from trivia import app, db
from .models import Category, Question, User

# questions pagination
QUESTIONS_PER_PAGE = 10


@app.after_request
def after(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
  return response

@app.route('/api/categories')
def get_all_categories():
  # get categories
  categories: List[Category] = Category.query.all()
  # todo says list of categories but react state works with an object/dictonary?
  category_obj: Dict[int, str] = {category.id: category.type for category in categories}
  categories_length = len(categories)
  
  if categories_length == 0:
    abort(404)
  
  return jsonify(
    {
      "success": True,
      "categories": category_obj,
      "total_categories": categories_length,
    }
  )

@app.route('/api/questions')
def get_paginated_questions():
  # get page
  page = request.args.get('page', 1, type=int)
  # calculate start and end of items in a page
  end_item = page * QUESTIONS_PER_PAGE
  start_item = end_item - (QUESTIONS_PER_PAGE - 1)
  # query
  questions: List[Question] = Question.query\
    .filter(Question.id.between(start_item, end_item)).all()
  all_categories: List[Category] = Category.query.all()
  # questions_categories: List[int] = [question.category for question in questions]
  # todo says list of categories but react state works with an object/dictonary?
  questions_categories: Dict[int] = {category.id: category.type for category in all_categories}
  total_questions = Question.query.count()
  questions_length = len(questions)
  
  if questions_length == 0:
    abort(404)
  
  return jsonify(
    {
      "success": True,
      "questions": [question.format() for question in questions],
      "categories": questions_categories,
      "total_questions": total_questions,
      "current_category": 'No idea yet', # current of? frontend code makes no use of this except for state value
    }
  )
  
@app.route('/api/questions', methods=['POST'])
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
    question_obj.insert()
  except Exception as e:
    abort(400)
  finally:
    db.session.close()
  
  return jsonify({
    "success": True,
  }), 201
  
@app.route('/api/categories', methods=['POST'])
def create_category():
  # vars
  category_type: str|None = request.get_json()["type"]
  
  # confirm valid query
  if category_type is None:
    # invalid query
    abort(422, "Missing Field: type")
    
  # confirm type doesnt exist
  catgry_check: Category|None  = Category.query.filter(Category.type == category_type).first()
  if catgry_check is not None:
    abort(400, "That Category already exists")
    
  # create
  new_category = Category(category_type)
  # add
  try:
    new_cat = new_category.insert()
    returned_data = new_cat.format()
  except Exception as error:
    # db error most likely, not sure what to tell the user...
    db.session.rollback()
    print(error)
    abort(503, "System busy, Cant process request")
  finally:
    db.session.close()
    
  return jsonify({
    "success": True,
    "category": returned_data
  }), 201
  
@app.route('/api/questions/<int:question_id>', methods=["DELETE"])
def delete_question(question_id: int):
  # get question
  question: Question | None = Question.query.get(question_id)
  
  if question is None:
    abort(404, "Item not found")
  
  data_id = question.id
  try:
    question.delete()
  except:
    # change this to db error later
    abort(404)
  finally:
    db.session.close()
    
  return jsonify({
    "success": True,
    "id": data_id
  }), 200
  
@app.route('/api/questions/search', methods=['POST'])
def search_questions():
  # get page
  search_term = request.get_json()['searchTerm']
  
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
    questions: List[Question] = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
  except Exception as err:
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
  
@app.route('/api/categories/<int:category_id>/questions')
def get_questions_by_category(category_id):
  # check if categorey exist
  category: Category|None = Category.query.get(category_id)
  
  if category is None:
    abort(400, 'Category does not exist')
    
  # query
  questions: List[Question] = Question.query.filter(Question.category == category_id).all()
  
  return jsonify(
    {
      "success": True,
      "questions": [question.format() for question in questions],
      "total_questions": len(questions)
    }
  )

@app.route('/api/quizzes', methods=['POST'])
def get_play_next_question():
  request_data = request.get_json()
  previous_questions = request_data['previous_questions']
  quiz_category_id = request_data['quiz_category']['id']
  
  if quiz_category_id is None:
    abort(422, "Quiz category missing")
    
  if quiz_category_id == 0:
    # user selected all, only filter id
    question = Question.query.filter(~Question.id.in_(previous_questions)).order_by(func.random()).limit(1).first()
  else:
    question = Question.query.filter(Question.category == int(quiz_category_id))\
      .filter(~Question.id.in_(previous_questions)).order_by(func.random()).limit(1).first()
  
  print(question)
  
  return jsonify(
    {
      "success": True,
      "question": question.format() if question is not None else False,
    }
  )

@app.route('/api/users/<username>')
def get_user(username):
  
  if username == "":
    # empty abort
    abort(422, "Username cant be empty string")
  
  # get user if exist
  user: User|None = User.query.filter(User.username == username).first()
  
  if user is None:
    abort(404, "User does not Exist")
    
  return jsonify({
    "success": True,
    "user": user.format()
  })

@app.route('/api/users', methods=['POST'])
def create_user():
  username = request.get_json()['username']
  
  if username == "":
    # empty abort
    abort(422, "Username cant be empty string")
  
  # get user if exist
  user: User|None = User.query.filter(User.username == username).first()
  
  if user is not None:
    # exists
    return jsonify({
      "success": True,
      "user": user.format()
    })
  
  # doesnt exist create
  new_user = User(username)
  try:
    new_user.insert()
    return_user = new_user.format()
  except Exception as error:
    print(error)
    db.session.rollback()
    abort(503, "Error creating that user")
  finally:
    db.session.close()
    
  return jsonify({
    "success": True,
    "user": return_user
  })
  
@app.route('/api/users/<int:user_id>/score', methods=['POST'])
def add_user_score(user_id):
  score = request.get_json()['score']
  
  # get user if exist
  user: User|None = User.query.get(user_id)
  
  if user is None:
    # error
    abort(404, "User does not exist")
    
  curr_score = [score for score in user.scores]
  curr_score.append(score)
  user.scores = curr_score
  try:
    _user = user.update()
    return_user = _user.format()
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


"""
@TODO:
Create an endpoint to handle GET requests
for all available categories.
"""

"""
@TODO:
Create an endpoint to handle GET requests for questions,
including pagination (every 10 questions).
This endpoint should return a list of questions,
number of total questions, current category, categories.

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions.
"""

"""
@TODO:
Create an endpoint to DELETE question using a question ID.

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page.
"""

"""
@TODO:
Create an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

TEST: When you submit a question on the "Add" tab,
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.
"""

"""
@TODO:
Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

TEST: Search by any phrase. The questions list will update to include
only question that include that string within their question.
Try using the word "title" to start.
"""

"""
@TODO:
Create a GET endpoint to get questions based on category.

TEST: In the "List" tab / main screen, clicking on one of the
categories in the left column will cause only questions of that
category to be shown.
"""

"""
@TODO:
Create a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions.

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not.
"""

"""
@TODO:
Create error handlers for all expected errors
including 404 and 422.
"""

@app.errorhandler(400)
def handle_400(error):
  # Bad Request
  print(error.description)
  return jsonify({
    "success": False,
    "message": error.description if error.description is not None else "Error in Query/Data",
    "error": 400
  }), 400

@app.errorhandler(422)
def handle_422(error):
  # bad syntax 
  print(error.description)
  return jsonify({
    "success": False,
    "message": error.description if error.description is not None else "Error in Query/Data",
    "error": 422
  }), 422
  
@app.errorhandler(404)
def handle_404(error):
  # Not Found 
  print(error.description)
  return jsonify({
    "success": False,
    "message": error.description if error.description is not None else "Resource not Found",
    "error": 404
  }), 404
  
@app.errorhandler(405)
def handle_405(error):
  # Method Not Allowed
  return jsonify({
    "success": False,
    "message": "Method not allowed",
    "error": 405
  }), 405
  
@app.errorhandler(503)
def handle_503(error):
  # Server cannot process the request
  return jsonify({
    "success": False,
    "message": "System Busy",
    "error": 503
  }), 503