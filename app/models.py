from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
# import requests

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable = False)
    last_name = db.Column(db.String(45), nullable = False)
    username = db.Column(db.String(45), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def saveChanges(self):
        db.session.commit()

