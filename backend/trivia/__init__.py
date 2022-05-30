'''
  holds setup init function and exports app,db
'''
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None, database_uri=None):
  '''
    create and configure the app
    global so imports from models and controllers work,
    also allows configuration from tests
  '''
  # i know global is unsafe but i need app exported whenever this func called
  # which i mainly form runpy, but i'm importing from here so no top level module import
  global app, db
  app = Flask(__name__)
  if test_config is None:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["DEBUG"] = True # for some reason causes an assertion error when set for testing
  else:
    app.config.from_mapping(test_config)
  
    
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db = SQLAlchemy(app)
  # import models before creating db so new tables can be created
  from . import models
  # now create
  db.create_all() # leaving this as i havent tweaked the sql script to create user table for now
  cors = CORS(app, resources={"r*/api/*":{"origins":"*"}})
  migrate = Migrate(app, db)
  return [app, db]

