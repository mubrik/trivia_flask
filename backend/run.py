'''
  top level module, starts app
'''
import os
from trivia import create_app
from dotenv import load_dotenv

# load env variables
load_dotenv()
# use .env or computer environment
database_uri = os.environ.get('DB_URI')

# create app db
app, db = create_app(database_uri=database_uri)

# import controllers to allow routes assignment
# importing late to allow global app creation
from trivia import controllers

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)