from werkzeug.security import check_password_hash, generate_password_hash

from project import db

from .models import User


def create_user(email, password):
    password_hash = generate_password_hash(password)
    user = User(email=email, password=password_hash)
    db.session.add(user)
    db.session.commit()


def allow_user_to_login(email, password):
    user = User.query.filter_by(email=email).first()
    check_password_hash(pwhash=user.password, password=password)
    return user
