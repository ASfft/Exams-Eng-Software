from flask import Blueprint, render_template
from flask_login import login_required

from app.constants import UserTypes
from app.models import Exam, Answer, User

bp = Blueprint("reports", __name__)


@bp.route('/<int:exam_id>/answers', methods=['GET'])
@login_required
def report_answers(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    answers = Answer.query.filter_by(exam_id=exam_id).all()
    students = User.query.filter(User.id.in_([a.student_id for a in answers])).all()
    return render_template('reports/answers.jinja2', exam=exam, students=students, answers=answers)


@bp.route('/<int:exam_id>/grades', methods=['GET'])
@login_required
def report_grades(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    students = User.query.filter_by(user_type_id=UserTypes.STUDENT).all()
    grades = [(student, exam.grade(student.id)) for student in students]
    return render_template('reports/grades.jinja2', exam=exam, grades=grades)
