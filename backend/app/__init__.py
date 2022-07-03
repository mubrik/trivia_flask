'''
  holds setup init function and exports app,db
'''
'''
  init file, set up the app
'''
import sys
import unittest
from os import environ as env
from typing import List
from unittest import TestCase
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# load env
load_dotenv()

# get env vars
RUN_MODE = env.get('FLASK_RUN_MODE', 'development')

# define WSGI app
app = Flask(__name__)

if RUN_MODE == 'development':
  # dev
  print('development mode')
  app.config.from_object('configs.development')
elif RUN_MODE == 'testing':
  print('testing mode')
  app.config.from_object('configs.testing')
else:
  raise NameError('unknown run mode, add FLASK_RUN_MODE to your env')

# Define the database object
db = SQLAlchemy(app)
# setup migration
migrate = Migrate(app, db)
# setup cors for api routes and specific origin
cors = CORS(app, resources={r"/api/*": {"CORS_ORIGINS": "http://127.0.0.1:3000/"}})
# jwt manager
jwt_manager = JWTManager(app)
# bcrypt
flask_bcrypt = Bcrypt(app)

# Import a module / component using its blueprint handler variable
from .user.controllers import user_bp as user_blueprint
from .trivia.controllers import trivia_bp as trivia_blueprint

# Register blueprint(s)
app.register_blueprint(user_blueprint, url_prefix='/api/')
app.register_blueprint(trivia_blueprint, url_prefix='/api/')

# import cli functons
from .utils import *

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

if RUN_MODE == 'testing':
  # import test cases
  from .user.tests import UserTestCase
  from .trivia.tests import TriviaTestCase
  test_list: List[TestCase] = [UserTestCase, TriviaTestCase]
  # run tests
  for test in test_list:
    suite = unittest.TestLoader().loadTestsFromTestCase(test)
    unittest.TextTestRunner(verbosity=2).run(suite)
  # exit
  sys.exit("Test Done")
