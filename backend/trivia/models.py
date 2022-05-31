'''
  holds the models of app
'''
from sqlalchemy import Column, String, Integer, ForeignKey, PickleType
from sqlalchemy.orm import relationship, backref
from trivia import db


class Question(db.Model):
  """
  Question

  """
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(Integer, ForeignKey('categories.id'), nullable=False)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

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
        'question': self.question,
        'answer': self.answer,
        'category': self.category,
        'difficulty': self.difficulty
    }


class Category(db.Model):
  """
  Category

  """
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)
  questions = relationship('Question', backref=backref(
      'category_item', lazy='joined'), lazy='select')

  def __init__(self, type):
    self.type = type

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
        'type': self.type
    }


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
