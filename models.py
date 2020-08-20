from project import db

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

import time


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    is_activated = db.Column(db.Boolean, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.is_activated = False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def activate(self):
        self.is_activated = True

    def __repr__(self):
        return 'User %d %s' % (self.id, self.username)


# TODO: Create your other models here
class Subject(db.Model):
    
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)

    def get_other_subjects(self):
        the_list = db.session.query(Subject).filter_by(user=self.user).all()
        the_list.remove(self)
        return the_list

    def __repr__(self):
        return self.subject

class Lesson(db.Model):

    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)

    def get_times_string(self):
        return time.asctime(time.gmtime(self.start_time))[11:16]+"-"+time.asctime(time.gmtime(self.end_time))[11:16]

    def get_subject(self):
        return db.session.query(Subject).filter_by(id=self.subject).first()

class Assignment(db.Model):

    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    d_date = db.Column(db.Integer, nullable=False)
    d_month = db.Column(db.Integer, nullable=False)
    d_year = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    is_done = db.Column(db.Boolean, nullable=False)

    def get_subject(self):
        return db.session.query(Subject).filter_by(id=self.subject).first()

    def deadline_passed(self):
        if time.mktime(time.struct_time([self.d_year,self.d_month,self.d_date+1,0,0,0,0,0,0]))-time.time()<0:
            return True
        else:
            return False

    # fill in the rest of your fields and methods!
