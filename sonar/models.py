from werkzeug import generate_password_hash, check_password_hash
import datetime
from sonar import db

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	username = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(54))
	registered_on = db.Column(db.DateTime)

	ideas = db.relationship('Idea', backref='user', lazy='dynamic')
	datasets = db.relationship('Dataset', backref='user', lazy='dynamic')

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

ideas_tags = db.Table('ideas_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('idea_id', db.Integer, db.ForeignKey('ideas.id')),
	db.PrimaryKeyConstraint('tag_id', 'idea_id'))

ideas_datasets = db.Table('ideas_datasets',
    db.Column('idea_id', db.Integer, db.ForeignKey('ideas.id')),
    db.Column('dataset_id', db.Integer, db.ForeignKey('datasets.id')),
	db.PrimaryKeyConstraint('idea_id', 'dataset_id'))

class Tag(db.Model):
	__tablename__ = 'tags'
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(100), unique=True)

class Idea(db.Model):
	__tablename__ = 'ideas'
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	scientificfield_id = db.Column(db.Integer, db.ForeignKey('scientificfields.id'))
	title = db.Column(db.String(100))
	question = db.Column(db.String(100))
	is_featured = db.Column(db.String(3))
	description = db.Column(db.String(10000))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_date = db.Column(db.DateTime)
	tags=db.relationship('Tag', secondary=ideas_tags, backref='ideas' )  
	datasets=db.relationship('Dataset', secondary=ideas_datasets, backref='ideas' )  

class Scientificfield(db.Model):
	__tablename__ = 'scientificfields'
	id = db.Column(db.Integer, primary_key = True)
	description = db.Column(db.String(200))
	ideas = db.relationship('Idea', backref='scientificfield', lazy='dynamic')

class Dataset(db.Model):
	__tablename__ = 'datasets'
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	title = db.Column(db.String(100))
	description = db.Column(db.String(1000))
	filename = db.Column(db.String(300))
	filename_disk = db.Column(db.String(350))
	filesize_bytes = db.Column(db.Float)
	license = db.Column(db.String(200))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())