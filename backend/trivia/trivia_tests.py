'''
  holds the test cases for trivia app
'''
import unittest
from flask_sqlalchemy import SQLAlchemy
from trivia import app, db


class ExtendedTestCase(unittest.TestCase):
  """This class represents the trivia test case"""
  
  def setUp(self):
    """Define test variables and initialize app."""
    app.testing = True
    self.app = app
    self.client = self.app.test_client
    # binds the app to the current context
    with self.app.app_context():
      # self.db = SQLAlchemy()
      # self.db.init_app(self.app)
      self.db = db
      # create all tables
      self.db.create_all()
  
  def tearDown(self):
    """Executed after reach test"""
    pass
  
  def test_get_categories(self):
    result = self.client().get('/api/categories')
    # checks, status code
    # on success, user gets categories over 1
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.get_json()['success'], True)
    self.assertGreater(result.get_json()['total_categories'], 0)
    
  def test_get_categories_error(self):
    result = self.client().get('/api/categorie')
    # checks, bad url
    # on bad or no data
    self.assertEqual(result.status_code, 404)
    self.assertEqual(result.get_json()['success'], False)
  
  def test_get_questions(self):
    result = self.client().get('/api/questions?page=2')
    # checks, status code
    # on success, user gets total_questions greater than 1
    self.assertEqual(result.get_json()['success'], True)
    self.assertGreater(result.get_json()['total_questions'], 0)
    
  def test_get_questions_test_error(self):
    result = self.client().get('/api/questions?page=60')
    # checks, status codedef __init__(self, app=None, *args, **kwargs) -> None:
  #   super(TriviaTestCase).__init__(*args, **kwargs)
  #   self.app = app
    # on paginating a page that dont exist
    self.assertEqual(result.status_code, 404)
    self.assertEqual(result.get_json()['success'], False)
    
  def test_create_question(self):
    self.new_question = {
      "question": "1 + 1 = ?", 
      "answer": "2", 
      "category": 2, 
      "difficulty": 1
    }
    # tests creating a simple question
    result = self.client().post('/api/questions', json=self.new_question)
    # checks
    self.assertEqual(result.status_code, 201)
    self.assertIn("question", result.get_json())
  
  def test_create_question_data_error(self):
    self.new_error_question = {
      "question": "1 + 1 = ?", 
      "answer": "2",
    }
    # tests creating a question with incomplete data
    result = self.client().post('/api/questions', json=self.new_error_question)
    # checks
    # 422, incomplete query
    self.assertEqual(result.status_code, 422)
  
  def test_delete_question(self):
    self.new_question = {
      "question": "7 + 7 = ?", 
      "answer": "14", 
      "category": 2, 
      "difficulty": 1
    }
    # tests create a new question first
    result_new = self.client().post('/api/questions', json=self.new_question)
    id = result_new.get_json()['question']['id']
    # then try deleteing it
    result = self.client().delete(f'/api/questions/{id}')
    # checks
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.get_json()['success'], True)
    self.assertEqual(result.get_json()['id'], id)
    
  def test_delete_question_error(self):
    result = self.client().delete('/api/questions/555525')
    # checks
    # deleteing something that dont exist, 404
    self.assertEqual(result.status_code, 404)
    self.assertEqual(result.get_json()['success'], False)

  def test_create_category(self):
    # tests creating a category
    self.new_category = {
      "type": "ChemistryTest",
    }
    result = self.client().post('/api/categories', json=self.new_category)
    id = result.get_json()['category']['id']
    # checks, code and category in returned object
    self.assertEqual(result.status_code, 201)
    self.assertIn("category", result.get_json())
    # delete the category,, should make this delete test?
    self.client().delete(f'/api/categories/{id}/delete')
    
  def test_create_exisiting_category_error(self):
    self.new_category = {
      "type": "Chemistry",
    }
    # create the category first
    result_new = self.client().post('/api/categories', json=self.new_category)
    id = result_new.get_json()['category']['id']
    # try creating the same categgory
    result = self.client().post('/api/categories', json=self.new_category)
    # checks, code and category in returned object
    self.assertEqual(result.status_code, 400)
    self.assertEqual(result.get_json()['message'], "That Category already exists")
    # delete it for continuity
    self.client().delete(f'/api/categories/{id}/delete')
    
  def test_search_questions(self):
    self.search_query = {
      "searchTerm": "title"
    }
    result = self.client().post('/api/questions/search', json=self.search_query)
    # checks
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.get_json()['success'], True)
    
  def test_get_questions_by_category(self):
    result = self.client().get('/api/categories/2/questions')
    # checks
    # checks status and questions in returned obj
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.get_json()['success'], True)
    self.assertIn("questions", result.get_json())
    
  def test_get_questions_by_category_error(self):
    result = self.client().get('/api/categories/80/questions')
    # checks
    # checks searching by category that doesnt exist
    self.assertEqual(result.status_code, 400)
    self.assertEqual(result.get_json()['success'], False)
    self.assertIn("message", result.get_json())
    self.assertEqual(result.get_json()['message'], "Category does not exist")
    
  def test_get_play_next_question(self):
    self.play_quiz_option = {
      "previous_questions": [4],
      "quiz_category": {"id": 3, "type": "Geography"}
    }
    result = self.client().post('/api/quizzes', json=self.play_quiz_option)
    # checks
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.get_json()['success'], True)
    self.assertIn("question", result.get_json())
  
  def test_get_user(self):
    # create user first
    post_result = self.client().post('/api/users', json={"username": "johntest"})
    id = post_result.get_json()['user']['id']
    # check
    result = self.client().get('/api/users/johntest')
    # checks
    self.assertEqual(result.status_code, 200)
    self.assertIn("user", result.get_json())
    # delete the user
    self.client().delete(f'/api/users/{id}/delete')
    
  def test_get_user_error(self):
    # create user first
    self.client().post('/api/users', json={"username": "johntest"})
    # check wrong user
    result = self.client().get('/api/users/johntt')
    # checks
    self.assertEqual(result.status_code, 404)
    self.assertIn("message", result.get_json())
    self.assertEqual(result.get_json()['message'], "User does not Exist")
    
  def test_create_user(self):
    # create user first
    result = self.client().post('/api/users', json={"username": "testing"})
    # checks, route checks if user exist and returns 200 but creates and return 201 when it doesnt
    id = result.get_json()['user']['id']
    self.assertEqual(result.status_code, 201)
    self.assertIn("user", result.get_json())
    # username == testing
    self.assertEqual(result.get_json()['user']['username'], "testing")
    # delete the user
    self.client().delete(f'/api/users/{id}/delete')
  
  def test_create_user_empty_error(self):
    # create user first
    result = self.client().post('/api/users', json={"username": ""})
    # checks
    self.assertEqual(result.status_code, 422)
    self.assertIn("message", result.get_json())
    self.assertEqual(result.get_json()['message'], "Username cant be empty string")
    