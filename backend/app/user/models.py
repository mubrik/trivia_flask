'''
  holds the models of user module
'''
from sqlalchemy import Column, String, Integer, PickleType
from app import db, flask_bcrypt, jwt_manager

class User(db.Model):
  """_summary_
    User class
  Returns:
    User: a SqlAlchemy Model class
  """
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  username = Column(String, unique=True)
  password_hash = Column(String(128))
  # should be a seperate class so store questions but...this will do
  scores = Column(PickleType, default=[], nullable=False)
  
  @property
  def password(self):
    raise AttributeError('password not readable')
  @password.setter
  def password(self, password: str):
    self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
  
  def verify_password(self, password: str):
    return flask_bcrypt.check_password_hash(self.password_hash, password)

  def __init__(self, username: str, password: str):
    self.username = username
    self.password = password

  def insert(self):
    db.session.add(self)
    db.session.commit()
    return self

  def update(self):
    db.session.commit()
    return self

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'username': self.username,
      'scores': self.scores
    }

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt_manager.user_identity_loader
def user_identity_lookup(user):
  return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt_manager.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
  identity = jwt_data["sub"]
  return User.query.filter_by(id=identity).one_or_none()