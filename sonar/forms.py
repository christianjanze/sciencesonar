from flask_wtf import Form
from flask import flash
from wtforms import BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileRequired
from sonar.models import db, User

class SignupForm(Form):
	firstname = StringField('First Name', [validators.Length(min=1, max=100)])
	lastname = StringField('Last Name', [validators.Length(min=1, max=100)])
	username = StringField('E-Mail Address', [validators.Length(min=1, max=120)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords must match')
	])
	confirm = PasswordField('Password Confirmation')
	accept_tos = BooleanField('I hereby accept the Terms of Service', [validators.DataRequired()])

	def validate(self):
		if User.query.filter_by(username = self.username.data.lower()).first():
			flash("Username is already in use", "danger")
			return False
		else:
			return True

class SigninForm(Form):
	username = StringField("Username",  [validators.Required("Please enter your username"), validators.Email("Please enter your yousername.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])

class IdeaForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=100)])
	description = StringField('Description', [validators.Length(min=1, max=100)], widget=TextArea())
	scientific_area = StringField('Scientific Area')
	scientific_subarea = StringField('Scienific Subarea')

class DatasetForm(Form):
	description = StringField('Description', widget=TextArea())
	dataset = FileField(validators=[FileRequired()])