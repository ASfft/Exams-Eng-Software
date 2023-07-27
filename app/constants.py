from enum import IntEnum


class UserTypes(IntEnum):
    STUDENT = 1
    PROFESSOR = 2


class QuestionTypes(IntEnum):
    MULTIPLE_CHOICE = 1
    TRUE_OR_FALSE = 2
    NUMERIC = 3
