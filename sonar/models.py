from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

	# Define relationships
	# todo add
	#datasets = db.relationship('Dataset', backref='User', lazy='dynamic')
	ideas = db.relationship('Idea', backref='User', lazy='dynamic')

	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

class Idea(db.Model):
	__tablename__ = 'ideas'
	iid = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.uid'))
	title = db.Column(db.String(100))
	description = db.Column(db.String(100))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
	#TODO: ADD FIELDS
	#scientific_area = db.Column(db.String(100))
	#scientific_subarea = db.Column(db.String(100))

	def __init__(self, title, description, user_id):
		self.title = title
		self.description = description
		self.user_id = user_id