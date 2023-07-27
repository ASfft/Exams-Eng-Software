from datetime import datetime, timedelta
from random import randint, sample, random

from app.constants import UserTypes, QuestionTypes
from app.factory import db
from app.models import UserType, QuestionType, User, Question, Exam, ExamQuestion, Answer
from app.wsgi import app


def initialize_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        for user_type in UserTypes:
            new_user_type = UserType(name=user_type.name)
            db.session.add(new_user_type)

        for question_type in QuestionTypes:
            new_question_type = QuestionType(name=question_type.name)
            db.session.add(new_question_type)

        users = [
            User(id=1, username="pedro", password="asdfg", user_type_id=UserTypes.PROFESSOR),
            User(id=2, username="ester", password="asdfg", user_type_id=UserTypes.STUDENT),
        ]

        questions = [
            Question(
                id=1,
                text="Qual a capital do Brasil?",
                question_type_id=QuestionTypes.MULTIPLE_CHOICE,
                data={
                    "choices": [
                        {"text": "Rio de Janeiro"},
                        {"text": "Brasília"},
                        {"text": "São Paulo"},
                        {"text": "Salvador"},
                        {"text": "Porto Alegre"},
                    ],
                    "answer": "Brasília",
                },
            ),
            Question(
                id=2,
                text="A moeda do Brasil é o Dólar?",
                question_type_id=QuestionTypes.TRUE_OR_FALSE,
                data={"answer": "False"}
            ),
            Question(
                id=3,
                text="Quantos estados existem no Brasil?",
                question_type_id=QuestionTypes.NUMERIC,
                data={"answer": 26}
            ),
            Question(
                id=4,
                text="Qual é o maior animal terrestre do mundo?",
                question_type_id=QuestionTypes.MULTIPLE_CHOICE,
                data={
                    "choices": [
                        {"text": "Baleia Azul"},
                        {"text": "Elefante Africano"},
                        {"text": "Girafa"},
                        {"text": "Tubarão Branco"},
                        {"text": "Hipopótamo"},
                    ],
                    "answer": "Elefante Africano",
                },
            ),
            Question(
                id=5,
                text="A linguagem de programação Python foi criada em 1991?",
                question_type_id=QuestionTypes.TRUE_OR_FALSE,
                data={"answer": "True"}
            ),
            Question(
                id=6,
                text="Quantas horas existem em um dia?",
                question_type_id=QuestionTypes.NUMERIC,
                data={"answer": 24}
            ),
            Question(
                id=7,
                text="Qual desses é um elemento químico?",
                question_type_id=QuestionTypes.MULTIPLE_CHOICE,
                data={
                    "choices": [
                        {"text": "Água"},
                        {"text": "Ouro"},
                        {"text": "Diamante"},
                        {"text": "Aço"},
                        {"text": "Sal"},
                    ],
                    "answer": "Ouro",
                },
            ),
            Question(
                id=8,
                text="A Terra é o quarto planeta do sistema solar?",
                question_type_id=QuestionTypes.TRUE_OR_FALSE,
                data={"answer": "False"}
            ),
            Question(
                id=9,
                text="Quantos lados tem um quadrado?",
                question_type_id=QuestionTypes.NUMERIC,
                data={"answer": 4}
            ),
            Question(
                id=10,
                text="Qual o idioma oficial da França?",
                question_type_id=QuestionTypes.MULTIPLE_CHOICE,
                data={
                    "choices": [
                        {"text": "Inglês"},
                        {"text": "Alemão"},
                        {"text": "Espanhol"},
                        {"text": "Francês"},
                        {"text": "Italiano"},
                    ],
                    "answer": "Francês",
                },
            ),
            Question(
                id=11,
                text="O ser humano possui 206 ossos?",
                question_type_id=QuestionTypes.TRUE_OR_FALSE,
                data={"answer": "True"}
            ),
            Question(
                id=12,
                text="Quantos dias tem a semana?",
                question_type_id=QuestionTypes.NUMERIC,
                data={"answer": 7}
            ),
            Question(
                id=13,
                text="Qual é o planeta mais próximo do sol?",
                question_type_id=QuestionTypes.MULTIPLE_CHOICE,
                data={
                    "choices": [
                        {"text": "Vênus"},
                        {"text": "Terra"},
                        {"text": "Marte"},
                        {"text": "Júpiter"},
                        {"text": "Mercúrio"},
                    ],
                    "answer": "Mercúrio",
                },
            ),
            Question(
                id=14,
                text="O café foi descoberto no século XV, na Etiópia?",
                question_type_id=QuestionTypes.TRUE_OR_FALSE,
                data={"answer": "True"}
            ),
            Question(
                id=15,
                text="Qual o valor da soma de 2 + 2?",
                question_type_id=QuestionTypes.NUMERIC,
                data={"answer": 4}
            )
        ]

        exams = [
            Exam(
                id=1,
                title="Aberto e não respondido 1",
                start_date=datetime.now(),
                duration=120
            ),
            Exam(
                id=2,
                title="Aberto e não respondido 2",
                start_date=datetime.now(),
                duration=180
            ),
            Exam(
                id=3,
                title="Aberto e respondido 1",
                start_date=datetime.now(),
                duration=120
            ),
            Exam(
                id=4,
                title="Aberto e respondido 2",
                start_date=datetime.now(),
                duration=180
            ),
            Exam(
                id=5,
                title="Agendado 1",
                start_date=datetime.now() + timedelta(days=1),
                duration=180
            ),
            Exam(
                id=6,
                title="Agendado 2",
                start_date=datetime.now() + timedelta(days=20),
                duration=180
            ),
            Exam(
                id=7,
                title="Encerrado e respondido 1",
                start_date=datetime.now() - timedelta(hours=3),
                duration=180
            ),
            Exam(
                id=8,
                title="Encerrado e respondido 2",
                start_date=datetime.now() - timedelta(days=3),
                duration=180
            ),
            Exam(
                id=9,
                title="Encerrado e não respondido 1",
                start_date=datetime.now() - timedelta(hours=3),
                duration=180
            ),
            Exam(
                id=10,
                title="Encerrado e não respondido 2",
                start_date=datetime.now() - timedelta(days=3),
                duration=180
            ),
        ]

        exam_questions = []
        answers = []
        for exam in exams:
            sample_questions = sample(questions, randint(3, 15))
            for question in sample_questions:
                exam_questions.append(ExamQuestion(
                    exam_id=exam.id,
                    question_id=question.id,
                    value=randint(1, 10)
                ))
            if "e respondido" in exam.title:
                for question in sample_questions:
                    correct_answer = question.data.get("answer")
                    match question.question_type_id:
                        case QuestionTypes.NUMERIC:
                            incorrect_answer = random()*100
                        case QuestionTypes.TRUE_OR_FALSE:
                            incorrect_answer = correct_answer != "True"
                        case QuestionTypes.MULTIPLE_CHOICE:
                            incorrect_answer = sample(question.data.get("choices"), 1)[0].get("text")
                    answer = question.data.get("answer") if random() <= 0.5 else ("" if random() <= 0.1 else incorrect_answer)
                    answers.append(Answer(
                        data=answer,
                        question_id=question.id,
                        exam_id=exam.id,
                        student_id=2
                    ))

        for entity in users + questions + exams + exam_questions + answers:
            db.session.add(entity)

        db.session.commit()

    print("Initialized successfully!")


if __name__ == "__main__":
    initialize_database()
