import datetime

from flask_login import UserMixin
from sqlalchemy import DateTime

from project import db
from project.network_interface.models import NetworkInterface

user_network_interface = db.Table(
    'user_network_interface',
    db.Column('created', db.DateTime, onupdate=datetime.datetime.now),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('network_interface_id', db.Integer, db.ForeignKey(
        'network_interface.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32), nullable=True)
    update = db.relationship('models.NetworkInterface',
                             secondary=user_network_interface,
                             backref='updated_by')
    is_active = db.Column(db.Boolean, default=True)
