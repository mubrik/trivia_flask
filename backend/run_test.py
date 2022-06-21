# '''
#   top level module, starts training tests
# '''
# import os
# import unittest
# from app import create_app
# from dotenv import load_dotenv

# # load env variables
# load_dotenv()

# # get test db uri
# database_uri = os.environ.get('TEST_DB_URI')

# # create test app, so trivia_test can import
# app, db = create_app({
#   "SQLALCHEMY_DATABASE_URI": database_uri
# })

# # import controllers so routes get added for testing
# from app import controllers
# # import the class with test cases
# from app.trivia_tests import ExtendedTestCase

# # run the testcases when file loaded as top level module
# if __name__ == "__main__":
#   unittest.main()