'''
  holds test cases for the user module
'''
import unittest
from app import app, db

class UserTestCase(unittest.TestCase):
  '''
    base class for user tests
  '''
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
    pass


  def tearDown(self):
    '''
      tear down
    '''
    pass
  
  def test_get_user(self):
    # create user first
    post_result = self.client().post(
        '/api/users', json={"username": "johntest"})
    new_id = post_result.get_json()['user']['id']
    # check
    result = self.client().get('/api/users/johntest')
    # checks
    self.assertEqual(result.status_code, 200)
    self.assertIn("user", result.get_json())
    # delete the user
    self.client().delete(f'/api/users/{new_id}/delete')

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
    new_id = result.get_json()['user']['id']
    self.assertEqual(result.status_code, 201)
    self.assertIn("user", result.get_json())
    # username == testing
    self.assertEqual(result.get_json()['user']['username'], "testing")
    # delete the user
    self.client().delete(f'/api/users/{new_id}/delete')

  def test_create_user_empty_error(self):
    # create user first
    result = self.client().post('/api/users', json={"username": ""})
    # checks
    self.assertEqual(result.status_code, 422)
    self.assertIn("message", result.get_json())
    self.assertEqual(result.get_json()[
                    'message'], "Username cant be empty string")
