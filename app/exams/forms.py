from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    BooleanField,
    SubmitField,
    DateTimeLocalField,
    FloatField,
)
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms_sqlalchemy.fields import QuerySelectField

from app.factory import db
from app.models import Question


class ExamForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    start_date = DateTimeLocalField(
        "Start Date", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    duration = IntegerField(
        "Duration (in minutes)", validators=[DataRequired(), NumberRange(min=1)]
    )
    closed = BooleanField("Closed")
    submit = SubmitField("Submit")


class ExamSearchForm(FlaskForm):
    title = StringField("Title", validators=[Optional()])
    submit = SubmitField("Search")


class AddQuestionForm(FlaskForm):
    question = QuerySelectField(
        "Question", query_factory=lambda: db.session.query(Question), get_label="name"
    )
    value = FloatField("Value", validators=[DataRequired(), NumberRange(min=0, max=10)])
    submit = SubmitField("Submit")
