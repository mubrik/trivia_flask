'''
  holds the test cases for trivia app
'''
import unittest

class ExtendedTestCase():
  """This class represents the trivia test case"""
  
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
    
  # def test_create_category(self):
  #   # tests creating a category
  #   result = self.client().post('/api/categories', json=self.new_category)
  #   # checks, code and category in returned object
  #   self.assertEqual(result.status_code, 201)
  #   self.assertIn("category", result.get_json())
    
  def test_create_exisiting_category_error(self):
    self.new_category = {
      "type": "Chemistry",
    }
    # tests creating a category
    result = self.client().post('/api/categories', json=self.new_category)
    # checks, code and category in returned object
    self.assertEqual(result.status_code, 400)
    self.assertEqual(result.get_json()['message'], "That Category already exists")
    
  # def test_delete_question(self):
  #   result = self.client().delete('/api/questions/29')
  #   # checks
  #   self.assertEqual(result.status_code, 200)
  #   self.assertEqual(result.get_json()['success'], True)
  #   self.assertEqual(result.get_json()['id'], 29)
    
  def test_delete_question_error(self):
    result = self.client().delete('/api/questions/4')
    # checks
    # deleteing something that dont exist, 404
    self.assertEqual(result.status_code, 404)
    self.assertEqual(result.get_json()['success'], False)
    
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
    
  def test(self):
    pass

# class TriviaTestCase(unittest.TestCase):
#   """This class represents the trivia test case"""
  
#   def __init__(self, app=None, *args, **kwargs) -> None:
#     super(TriviaTestCase).__init__(*args, **kwargs)
#     self.app = app

#   def setUp(self):
#     """Define test variables and initialize app."""
#     # self.app = create_app()
#     self.client = self.app.test_client
#     # self.database_name = "trivia_test"
#     # self.database_path = 'postgresql://{}:{}@{}/{}'.format('mubrik', 'postgres','localhost:5432', self.database_name)
#     # setup_db(self.app, self.database_path)
#     self.new_question = {
#       "question": "1 + 1 = ?", 
#       "answer": "2", 
#       "category": 2, 
#       "difficulty": 1
#     }
#     self.new_error_question = {
#       "question": "1 + 1 = ?", 
#       "answer": "2",
#     }
#     self.new_category = {
#       "type": "Chemistry",
#     }
#     self.play_quiz_option = {
#       "previous_questions": [4],
#       "quiz_category": {"id": 3, "type": "Geography"}
#     }
#     self.search_query = {
#       "searchTerm": "title"
#     }

#     # binds the app to the current context
#     with self.app.app_context():
#       self.db = SQLAlchemy()
#       self.db.init_app(self.app)
#       # create all tables
#       self.db.create_all()
  
#   def tearDown(self):
#     """Executed after reach test"""
#     pass
  
#   def test_(self):
#     pass
  
#   def test_get_categories(self):
#     result = self.client().get('/api/categories')
#     # checks, status code
#     # on success, user gets categories over 1
#     self.assertEqual(result.status_code, 200)
#     self.assertEqual(result.get_json()['success'], True)
#     self.assertGreater(result.get_json()['total_categories'], 0)
    
#   def test_get_categories_error(self):
#     result = self.client().get('/api/categorie')
#     # checks, bad url
#     # on bad or no data
#     self.assertEqual(result.status_code, 404)
#     self.assertEqual(result.get_json()['success'], False)
  
#   def test_get_questions(self):
#     result = self.client().get('/api/questions?page=2')
#     # checks, status code
#     # on success, user gets total_questions greater than 1
#     self.assertEqual(result.get_json()['success'], True)
#     self.assertGreater(result.get_json()['total_questions'], 0)
    
#   def test_get_questions_test_error(self):
#     result = self.client().get('/api/questions?page=60')
#     # checks, status code
#     # on paginating a page that dont exist
#     self.assertEqual(result.status_code, 404)
#     self.assertEqual(result.get_json()['success'], False)
    
#   def test_create_question(self):
#     # tests creating a simple question
#     result = self.client().post('/api/questions', json=self.new_question)
#     # checks
#     self.assertEqual(result.status_code, 201)
  
#   def test_create_question_data_error(self):
#     # tests creating a question with incomplete data
#     result = self.client().post('/api/questions', json=self.new_error_question)
#     # checks
#     # 422, incomplete query
#     self.assertEqual(result.status_code, 422)
    
#   # def test_create_category(self):
#   #   # tests creating a category
#   #   result = self.client().post('/api/categories', json=self.new_category)
#   #   # checks, code and category in returned object
#   #   self.assertEqual(result.status_code, 201)
#   #   self.assertIn("category", result.get_json())
    
#   def test_create_exisiting_category_error(self):
#     # tests creating a category
#     result = self.client().post('/api/categories', json=self.new_category)
#     # checks, code and category in returned object
#     self.assertEqual(result.status_code, 400)
#     self.assertEqual(result.get_json()['message'], "That Category already exists")
    
#   # def test_delete_question(self):
#   #   result = self.client().delete('/api/questions/29')
#   #   # checks
#   #   self.assertEqual(result.status_code, 200)
#   #   self.assertEqual(result.get_json()['success'], True)
#   #   self.assertEqual(result.get_json()['id'], 29)
    
#   def test_delete_question_error(self):
#     result = self.client().delete('/api/questions/4')
#     # checks
#     # deleteing something that dont exist, 404
#     self.assertEqual(result.status_code, 404)
#     self.assertEqual(result.get_json()['success'], False)
    
#   def test_search_questions(self):
#     result = self.client().post('/api/questions/search', json=self.search_query)
#     # checks
#     self.assertEqual(result.status_code, 200)
#     self.assertEqual(result.get_json()['success'], True)
    
#   def test_get_questions_by_category(self):
#     result = self.client().get('/api/categories/2/questions')
#     # checks
#     # checks status and questions in returned obj
#     self.assertEqual(result.status_code, 200)
#     self.assertEqual(result.get_json()['success'], True)
#     self.assertIn("questions", result.get_json())
    
#   def test_get_questions_by_category_error(self):
#     result = self.client().get('/api/categories/80/questions')
#     # checks
#     # checks searching by category that doesnt exist
#     self.assertEqual(result.status_code, 400)
#     self.assertEqual(result.get_json()['success'], False)
#     self.assertIn("message", result.get_json())
#     self.assertEqual(result.get_json()['message'], "Category does not exist")
    
#   def test_get_play_next_question(self):
#     result = self.client().post('/api/quizzes', json=self.play_quiz_option)
#     # checks
#     self.assertEqual(result.status_code, 200)
#     self.assertEqual(result.get_json()['success'], True)
#     self.assertIn("question", result.get_json())
#   """
#   TODO
#   Write at least one test for each test for successful operation and for expected errors.
#   """


# Make the tests conveniently executable
# if __name__ == "__main__":
#   unittest.main()