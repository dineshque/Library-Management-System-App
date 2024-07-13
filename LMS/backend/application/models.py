from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=False, nullable = False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    last_visited = db.Column(db.DateTime(timezone=True),default=datetime.now(pytz.timezone('Asia/Kolkata')))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
  
class Section(db.Model):
    __tablename__ = 'section'
    section_id = db.Column(db.Integer(),autoincrement=True, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    date = db.Column(db.DateTime(timezone=True),default=datetime.now(pytz.timezone('Asia/Kolkata')))
    description = db.Column(db.String(255))
    books = db.relationship('Book', backref='section', lazy=True)

    
class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    author = db.Column(db.String(80))
    content = db.Column(db.String(255))
    rated = db.Column(db.Integer(), nullable = True)
    pages =  db.Column(db.Integer(), nullable = False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.section_id'), nullable=False)
    
class UserBook(db.Model):
  __tablename__ = 'userbook'
  book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False,primary_key=True)
  issued_date = db.Column(db.Date(), nullable=True)
  return_date = db.Column(db.Date(),nullable=True)
  days = db.Column(db.Integer(), nullable = False)
  book_status = db.Column(db.Integer())
  rate = db.Column(db.Integer())
  user = db.relationship('User', backref='users')
  book = db.relationship('Book', backref='books')