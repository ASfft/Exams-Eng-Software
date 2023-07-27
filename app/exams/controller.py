from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required

from .forms import ExamForm, ExamSearchForm, AddQuestionForm
from ..factory import db
from ..models import Exam, ExamQuestion, Question, Answer

bp = Blueprint("exams", __name__)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = ExamForm()
    if form.validate_on_submit():
        exam = Exam(
            title=form.title.data,
            start_date=form.start_date.data,
            duration=form.duration.data,
        )
        db.session.add(exam)
        db.session.commit()
        flash("Your exam has been created!", "success")
        return redirect(url_for("exams.search"))
    return render_template("exams/form.jinja2", title="New Exam", form=form)


@bp.route("/update/<int:exam_id>", methods=["GET", "POST"])
@login_required
def update(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    form = ExamForm()
    if form.validate_on_submit():
        exam.title = form.title.data
        exam.start_date = form.start_date.data
        exam.duration = form.duration.data
        db.session.commit()
        flash("Your exam has been updated!", "success")
        return redirect(url_for("exams.view_exams"))
    elif request.method == "GET":
        form.title.data = exam.title
        form.start_date.data = exam.start_date
        form.duration.data = exam.duration
    return render_template("exams/form.jinja2", title="Update Exam", form=form)


@bp.route("/delete/<int:exam_id>", methods=["POST"])
@login_required
def delete(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    db.session.delete(exam)
    db.session.commit()
    flash("Your exam has been deleted!", "success")
    return redirect(url_for("exams.view_exams"))


@bp.route("/<int:exam_id>/update_questions", methods=["GET"])
@login_required
def update_questions(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    exam_questions = ExamQuestion.query.filter_by(exam_id=exam.id).all()
    questions = Question.query.all()
    return render_template(
        "exams/update_questions.jinja2",
        title="Exam View",
        exam=exam,
        exam_questions=exam_questions,
        questions=questions,
    )


@bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    search_form = ExamSearchForm(request.form)
    exams = None
    if not search_form.title.data:
        exams = Exam.query.all()
    elif request.method == "POST" and search_form.validate():
        exams = Exam.query.filter(
            Exam.title.like("%" + search_form.title.data + "%")
        ).all()
    return render_template(
        "exams/search.jinja2", title="Search Exam", form=search_form, exams=exams
    )


@bp.route("/<int:exam_id>/add_existing_question", methods=["POST"])
@login_required
def add_question(exam_id):
    add_question_form = AddQuestionForm(request.form)
    exam = Exam.query.get_or_404(exam_id)
    exam_question = ExamQuestion.query.filter_by(
        exam_id=exam_id, question_id=add_question_form.question.data.id
    ).first()

    if add_question_form.question is None:
        flash("Error: No such question.", "error")
        return redirect(url_for("exams.view", exam_id=exam_id))

    if exam_question:
        flash("Error: Question already in exam.", "error")
    else:
        new_exam_question = ExamQuestion()
        new_exam_question.exam_id = exam_id
        new_exam_question.question_id = add_question_form.question.data.id
        new_exam_question.value = add_question_form.value.data
        db.session.add(new_exam_question)
        db.session.commit()
        flash("Question added to exam successfully.", "success")

    return redirect(url_for("exams.update_questions", exam_id=exam_id))


@bp.route("/<int:exam_id>/details", methods=["GET"])
@login_required
def details(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    return render_template(
        "exams/details.jinja2", exam=exam, current_time=datetime.now()
    )


@bp.route("/<int:exam_id>")
@login_required
def view_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    now = datetime.now()
    if now < exam.start_date:
        flash("This exam is not open.")
        return redirect(url_for("exams.details", exam_id=exam_id))
    answers = {}
    for exam_question in exam.exam_questions:
        exam_answer = Answer.query.filter_by(
            exam_id=exam_id,
            question_id=exam_question.question_id,
            student_id=current_user.id
        ).first()
        if exam_answer:
            answer = exam_answer.data
        else:
            answer = None
        answers[exam_question.question_id] = answer

    return render_template(
        "exams/view.jinja2",
        exam=exam,
        questions=[{**exam_question.question.as_json(), "value": exam_question.value} for exam_question in exam.exam_questions],
        answers=answers,
        time_left=(exam.end_date() - datetime.now()).seconds,
    )


@bp.route('/<int:exam_id>/submit_answer', methods=['POST'])
@login_required
def submit_answer(exam_id):
    data = request.get_json()
    question_id = data['questionId']
    answer = data.get("answer", "")
    exam = Exam.query.get_or_404(exam_id)
    now = datetime.now()
    if now > exam.end_date() or now < exam.start_date:
        flash("This exam is not open.")
        return redirect(url_for("exams.details", exam_id=exam_id))
    exam_answer = Answer.query.filter_by(exam_id=exam_id, question_id=question_id, student_id=current_user.id).first()
    if exam_answer:
        exam_answer.data = answer
        db.session.commit()
    else:
        new_answer = Answer()
        new_answer.data = answer
        new_answer.exam_id = exam_id
        new_answer.question_id = question_id
        new_answer.student_id = current_user.id
        db.session.add(new_answer)
        db.session.commit()
    return jsonify({'status': 'success'})
