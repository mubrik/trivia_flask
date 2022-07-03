import os
from os import environ as env
from dotenv import load_dotenv

# loadenv variable
load_dotenv()

# Statement for enabling the development environment
DEBUG = False # false for testing
# Get URI from environment variable
TEST_DB_URI = env.get('TEST_DB_URI', None)
# db path
SQLALCHEMY_DATABASE_URI = TEST_DB_URI
# print queries if debug
SQLALCHEMY_ECHO = False
# over head
SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies, not secure.. testing only
SECRET_KEY = env.get('SECRET_KEY', os.urandom(32))

# flask-jwt
JWT_SECRET_KEY = env.get('JWT_SECRET_KEY', os.urandom(32))
JWT_TOKEN_LOCATION = ["headers", "cookies"]
JWT_COOKIE_SECURE = False if DEBUG else True # only send cookies over https, true for production

# bcrypt
BCRYPT_HANDLE_LONG_PASSWORDS = True