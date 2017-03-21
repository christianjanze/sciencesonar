from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import datetime
from flask_login import LoginManager
 
db = SQLAlchemy()
login_manager = LoginManager()

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	username = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(54))
	registered_on = db.Column(db.DateTime)

	ideas = db.relationship('Idea', backref='User', lazy='dynamic')
	datasets = db.relationship('Dataset', backref='User', lazy='dynamic')

	def __init__(self, firstname, lastname, username, password):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.username = username.lower()
		self.set_password(password)
		self.registered_on = datetime.datetime.utcnow()

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def __repr__(self):
		return '<User %r>' % (self.username)

class Idea(db.Model):
	__tablename__ = 'ideas'
	iid = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	title = db.Column(db.String(100))
	description = db.Column(db.String(100))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
	scientific_area_id = db.Column(db.Integer)
	scientific_subarea_id = db.Column(db.Integer)

	def __init__(self, title, description, user_id, scientific_area_id, scientific_subarea_id):
		self.description = description
		self.title = title
		self.description = description
		self.user_id = user_id
		self.scientific_area_id = scientific_area_id
		self.scientific_subarea_id = scientific_subarea_id

class Dataset(db.Model):
	__tablename__ = 'datasets'
	did = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	description = db.Column(db.String(2000))
	filename = db.Column(db.String(300))
	filename_disk = db.Column(db.String(350))
	filesize_bytes = db.Column(db.Float)
	license = db.Column(db.String(200))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
	

	def __init__(self, description, filename, filename_disk, filesize_bytes, license, user_id):
		self.filename = filename
		self.filename_disk = filename_disk
		self.filesize_bytes = filesize_bytes
		self.license = license
		self.user_id = user_id
	