from flask_wtf import Form
from flask import flash
from wtforms import BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileRequired
from sonar.models import db, User

class SignupForm(Form):
	firstname = StringField('First Name', [validators.Length(min=1, max=100)])
	lastname = StringField('Last Name', [validators.Length(min=1, max=100)])
	email = StringField('E-Mail Address', [validators.Length(min=1, max=120)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords must match')
	])
	confirm = PasswordField('Password Confirmation')
	accept_tos = BooleanField('I hereby accept the Terms of Service', [validators.DataRequired()])

	def validate(self):
		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user:
			flash("E-Mail address is already in use", "danger")
			return False
		else:
			return True

class SigninForm(Form):
	email = StringField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])

	def validate(self):
		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			return False

class IdeaForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=100)])
	description = StringField('Description', [validators.Length(min=1, max=100)], widget=TextArea())
	scientific_area = StringField('Scientific Area')
	scientific_subarea = StringField('Scienific Subarea')

class DatasetForm(Form):
	description = StringField('Description', widget=TextArea())
	dataset = FileField(validators=[FileRequired()])