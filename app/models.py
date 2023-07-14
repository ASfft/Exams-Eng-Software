from datetime import datetime

from flask_login import UserMixin
from app.factory import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.id'), nullable=False)

    user_type = db.relationship('UserType', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.username


class UserType(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<UserType %r>' % self.name


class ExamQuestion(db.Model):
    __tablename__ = 'exam_questions'
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    exam = db.relationship('Exam', back_populates='exam_questions')
    question = db.relationship('Question')


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=False)
    closed = db.Column(db.Boolean, nullable=False, default=False)
    exam_questions = db.relationship('ExamQuestion', back_populates='exam')

    def __repr__(self):
        return f'<Exam {self.title}>'


class QuestionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<QuestionType {self.name}>'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=True)  # Correct answer
    question_type_id = db.Column(db.Integer, db.ForeignKey('question_type.id'), nullable=False)

    def __repr__(self):
        return f'<Question {self.text}>'


class StudentAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Assuming 'user' table for students

    question = db.relationship('Question')
    exam = db.relationship('Exam')
    student = db.relationship('User')  # Assuming 'User' model for students

    def __repr__(self):
        return f'<StudentAnswer {self.id}>'
