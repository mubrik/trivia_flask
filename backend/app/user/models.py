'''
  holds the models of user module
'''
from sqlalchemy import Column, String, Integer, PickleType
from app import db

class User(db.Model):
  """_summary_
    User class
  Returns:
    User: a SqlAlchemy Model class
  """
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  username = Column(String, unique=True)
  # should be a seperate class so store questions but...this will do
  scores = Column(PickleType, default=[], nullable=False)

  def __init__(self, username):
    self.username = username

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
