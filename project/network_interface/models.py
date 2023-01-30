import datetime
import enum

from project import db


class NetworkInterfaceType(enum.Enum):
    ipv4 = 'Ipv4'
    ipv6 = 'Ipv6'


class NetworkInterface(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)
    name = db.Column(db.String(12), nullable=False, unique=True)
    ip_address = db.Column(db.String(128), nullable=False)
    ip_type = db.Column(db.Enum(NetworkInterfaceType), nullable=False)
    prefix = db.Column(db.String(8), nullable=False)
    is_enable = db.Column(db.Boolean)
