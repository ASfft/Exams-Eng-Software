from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Optional
from wtforms_sqlalchemy.fields import QuerySelectField

from app.factory import db
from app.models import QuestionType


def get_question_types():
    return db.session.query(QuestionType)


class QuestionForm(FlaskForm):
    question_type = QuerySelectField(
        "Question Type", query_factory=get_question_types, get_label="name"
    )
    text = TextAreaField("Text", validators=[DataRequired()])
    data = TextAreaField("Data (JSON)", validators=[DataRequired()])
    submit = SubmitField("Submit")


class QuestionSearchForm(FlaskForm):
    search = StringField("Search", validators=[Optional()])
    submit = SubmitField("Search")
