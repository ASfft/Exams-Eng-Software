from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from .forms import QuestionForm, QuestionSearchForm
from ..factory import db
from ..models import Question, QuestionType

bp = Blueprint("questions", __name__)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            text=form.text.data,
            data=form.data.data,
            question_type_id=form.question_type.data.id,
        )
        db.session.add(question)
        db.session.commit()
        flash("Your question has been created!", "success")
        return redirect(url_for("questions.search"))
    return render_template(
        "questions/form.jinja2", title="New Question", form=form, is_update=False
    )


@bp.route("/update/<int:question_id>", methods=["GET", "POST"])
@login_required
def update(question_id):
    question = Question.query.get_or_404(question_id)
    form = QuestionForm()
    if form.validate_on_submit():
        question.text = form.text.data
        question.data = form.data.data
        question.question_type_id = form.question_type.data.id
        db.session.commit()
        flash("Your question has been updated!", "success")
        return redirect(url_for("questions.search"))
    elif request.method == "GET":
        form.text.data = question.text
        form.question_type.data = QuestionType.query.get(question.question_type_id)
        form.data.data = question.data
    return render_template(
        "questions/form.jinja2",
        title="Update Question",
        form=form,
        is_update=True,
        question_id=question_id,
    )


@bp.route("/delete/<int:question_id>", methods=["POST"])
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash("Your question has been deleted!", "success")
    return redirect(url_for("questions.search"))


@bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    search_form = QuestionSearchForm(request.form)
    questions = None
    if not search_form.search.data:
        questions = Question.query.all()
    elif request.method == "POST" and search_form.validate():
        questions = Question.query.filter(
            Question.json.like("%" + search_form.search.data + "%")
        ).all()
    return render_template(
        "questions/search.jinja2",
        title="Search Question",
        form=search_form,
        questions=questions,
    )
