from app.constants import UserTypes
from app.factory import db
from app.models import UserType
from app.wsgi import app


def initialize_database():
    with app.app_context():
        for user_type in UserTypes:
            new_user_type = UserType(name=user_type.name)
            db.session.add(new_user_type)

        db.session.commit()


if __name__ == '__main__':
    initialize_database()