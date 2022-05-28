import os
import unittest
from trivia.trivia_tests import ExtendedTestCase
from trivia import create_app
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# load env variables
load_dotenv()
# get db uri
database_uri = os.environ.get('TEST_DB_URI')
# create test app
app, db = create_app({
  "SQLALCHEMY_DATABASE_URI": database_uri
})
# import controllers so routes get added for testing
from trivia import controllers

# extend trivia testing routes
class BaseTestCase(unittest.TestCase, ExtendedTestCase):
  __test__ = False
  
  def setUp(self):
    """Define test variables and initialize app."""
    self.app = app
    self.client = self.app.test_client
    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()
  
  def tearDown(self):
    """Executed after reach test"""
    pass

# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()