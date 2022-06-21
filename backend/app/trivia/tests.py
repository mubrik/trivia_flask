'''
  holds test cases for the trivia module
'''
from typing import Tuple
import unittest
from app import app, db

class TriviaTestCase(unittest.TestCase):
  '''
    base class for trivia tests
  '''
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # variables for tests
    self.new_question = {
      "question": "1 + 1 = ?",
      "answer": "2",
      "difficulty": 1
    }
    self.new_category = {
      "type": "ChemistryTest",
    }
    self.new_error_question = {
      "question": "1 + 1 = ?",
      "answer": "2",
    }
    
  def setUp(self):
    '''
      set up
      Define test variables and initialize app.
    '''
    app.testing = True
    self.app = app
    self.client = self.app.test_client
    # binds the app to the current context
    with self.app.app_context():
      self.db = db 
      # create all tables
      self.db.create_all()
    


  def tearDown(self):
    '''
      tear down
    '''
    pass
  
  # repeating this so much i decided to create a function
  def create_new_category(self) -> int:
    # create the category first
    cat_result = self.client().post('/api/categories', json=self.new_category)
    new_cat_id = cat_result.get_json()['category']['id']
    return new_cat_id
  
  def create_new_question(self) -> Tuple[int, int]:
    # category first
    new_cat_id = self.create_new_category()
    # create a question
    new_question = dict.copy(self.new_question)
    new_question['category'] = new_cat_id
    print('new question:', new_question)
    # tests creating a simple question
    result = self.client().post('/api/questions', json=new_question)
    new_question_id = result.get_json()['question']['id']
    return [new_question_id, new_cat_id]
    
  
  def test_get_categories(self):
    # get the id of a new category
    new_cat_id: int = self.create_new_category()
    result = self.client().get('/api/categories')
    # delete category
    self.client().delete(f'/api/categories/{new_cat_id}')
    # checks, status code
    # on success, user gets categories over 1
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.get_json()['success'], True)
    self.assertGreater(result.get_json()['total_categories'], 0)
    
  def test_get_categories_error(self):
    result = self.client().get('/api/categorie')
    # checks, bad url
    # on bad
    self.assertEqual(result.status_code, 404)

  def test_get_questions(self):
    result = self.client().get('/api/questions?page=1')
    # checks, status code
    # on success, returns success and questions
    self.assertEqual(result.get_json()['success'], True)
    self.assertEqual(type(result.get_json()['questions']), list)

  def test_get_questions_test_error(self):
    result = self.client().get('/api/questions?page=60')
    # on paginating a page that dont exist
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.get_json()['success'], True)
    # but emty list
    self.assertEqual(result.get_json()['questions'], [])

  def test_create_question(self):
    # get the id of new category
    new_cat_id: int = self.create_new_category()
    # create a question
    new_question = dict.copy(self.new_question)
    new_question['category'] = new_cat_id
    print('new question:', new_question)
    # tests creating a simple question
    result = self.client().post('/api/questions', json=new_question)
    new_question_id = result.get_json()['question']['id']
    # delete the question and category
    self.client().delete(f'/api/questions/{new_question_id}')
    self.client().delete(f'/api/categories/{new_cat_id}')
    # checks
    self.assertEqual(result.status_code, 201)
    self.assertIn("question", result.get_json()) 

  def test_create_question_data_error(self):
    # tests creating a question with incomplete data
    result = self.client().post('/api/questions', json=self.new_error_question)
    # checks
    # 422, incomplete query
    self.assertEqual(result.status_code, 422)

  def test_delete_question(self):
    # get the id of new category
    new_cat_id: int = self.create_new_category()
    # create a question
    new_question = dict.copy(self.new_question)
    new_question['category'] = new_cat_id
    # tests creating a simple question
    quest_result = self.client().post('/api/questions', json=new_question)
    new_question_id = quest_result.get_json()['question']['id']
    # then try deleteing it
    result = self.client().delete(f'/api/questions/{new_question_id}')
    # delete category
    self.client().delete(f'/api/categories/{new_cat_id}')
    # checks
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.get_json()['success'], True)
    self.assertEqual(result.get_json()['id'], new_question_id)
    

  def test_delete_question_error(self):
    result = self.client().delete('/api/questions/555525')
    # checks
    # deleteing something that dont exist, 404
    self.assertEqual(result.status_code, 404)
    self.assertEqual(result.get_json()['success'], False)

  def test_create_category(self):
    # tests creating a category
    result = self.client().post('/api/categories', json=self.new_category)
    new_id = result.get_json()['category']['id']
    # delete the category,
    self.client().delete(f'/api/categories/{new_id}')
    # checks, code and category in returned object
    self.assertEqual(result.status_code, 201)
    self.assertIn("category", result.get_json())
    

  def test_create_exisiting_category_error(self):
    # create the category first
    new_cat_id: int = self.create_new_category()
    # try creating the same categgory
    result = self.client().post('/api/categories', json=self.new_category)
    # delete it for continuity
    self.client().delete(f'/api/categories/{new_cat_id}')
    # checks, code and category in returned object
    self.assertEqual(result.status_code, 400)
    self.assertEqual(result.get_json()[
                     'message'], "That Category already exists")
    

  def test_search_questions(self):
    self.search_query = {
      "searchTerm": "title"
    }
    result = self.client().post('/api/questions/search', json=self.search_query)
    # checks
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.get_json()['success'], True)

  def test_get_questions_by_category(self):
    # get the id of new category
    new_cat_id: int = self.create_new_category()
    result = self.client().get(f'/api/categories/{new_cat_id}/questions')
    # delete category for continuity
    self.client().delete(f'/api/categories/{new_cat_id}')
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
    # create new quest and category
    new_quest_id, new_cat_id = self.create_new_question()
    play_object = {
      "previous_questions": [new_quest_id],
      "quiz_category": {"id": new_cat_id, "type": "ChemistryTest"}
    }
    # post
    result = self.client().post('/api/quizzes', json=play_object)
    # delete the question and category
    self.client().delete(f'/api/questions/{new_quest_id}')
    self.client().delete(f'/api/categories/{new_cat_id}')
    # checks
    self.assertEqual(result.status_code, 200)
    self.assertEqual(result.get_json()['success'], True)
    self.assertIn("question", result.get_json())