'''
  holds the models of trivia module
'''
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from app import db


class Question(db.Model):
  """
  Question
  Returns:
    Question: a SqlAlchemy Model class
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
  Returns:
    category: a SqlAlchemy Model class
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

