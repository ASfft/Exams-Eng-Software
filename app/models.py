from datetime import datetime, timedelta

from flask_login import UserMixin

from app.constants import UserTypes
from app.factory import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type_id = db.Column(db.Integer, db.ForeignKey("user_type.id"), nullable=False)

    user_type = db.relationship("UserType", backref=db.backref("users", lazy=True))

    def __repr__(self):
        return "<User %r>" % self.username

    def is_student(self) -> bool:
        return self.user_type_id == UserTypes.STUDENT

    def is_professor(self) -> bool:
        return self.user_type_id == UserTypes.PROFESSOR


class UserType(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return "<UserType %r>" % self.name


class ExamQuestion(db.Model):
    __tablename__ = "exam_questions"
    exam_id = db.Column(db.Integer, db.ForeignKey("exam.id"), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    exam = db.relationship("Exam", back_populates="exam_questions")
    question = db.relationship("Question")


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=False)
    exam_questions = db.relationship("ExamQuestion", back_populates="exam")

    def __repr__(self):
        return f"<Exam {self.title}>"

    def end_date(self) -> datetime:
        return self.start_date + timedelta(minutes=self.duration)

    def has_ended(self) -> bool:
        return datetime.now() > self.end_date()

    def grade(self, student_id: int) -> dict:
        answers = Answer.query.filter_by(exam_id=self.id, student_id=student_id).all()
        questions_values = {exam_question.question.id: exam_question.value for exam_question in self.exam_questions}
        grade = 0
        total = sum(questions_values.values())
        for answer in answers:
            if answer.is_correct():
                grade += questions_values[answer.question_id]
        return {"grade": grade, "total": total}

    def grade_as_string(self, student_id: int) -> str:
        grade = self.grade(student_id)
        return f"{grade['grade']} / {grade['total']}"

    def as_json(self) -> dict:
        return {
            "id": self.id,
            "tile": self.title,
            "start_date": self.start_date.isoformat(),
            "duration": self.duration,
            "exam_questions": [
                exam_question.question.as_json()
                for exam_question in self.exam_questions
            ],
        }


class QuestionType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<QuestionType {self.name}>"

    def pretty_name(self):
        return self.name.replace("_", " ").title()


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.JSON, nullable=False)
    text = db.Column(db.String(1000), nullable=True)
    question_type_id = db.Column(
        db.Integer, db.ForeignKey("question_type.id"), nullable=False
    )
    question_type = db.relationship("QuestionType")

    def __repr__(self):
        return f"<Question {self.text}>"

    def as_json(self) -> dict:
        return {
            "id": self.id,
            "data": self.data,
            "text": self.text,
            "question_type": {
                "id": self.question_type.id,
                "name": self.question_type.pretty_name(),
            },
        }


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, nullable=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("exam.id"), nullable=False)
    student_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )

    question = db.relationship("Question")
    exam = db.relationship("Exam")
    student = db.relationship("User")

    def __repr__(self):
        return f"<StudentAnswer {self.id}>"

    def is_correct(self) -> bool:
        return self.question.data.get("answer") == self.data
