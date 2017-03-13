from flask_wtf import Form
from flask import flash
from wtforms import BooleanField, TextField, PasswordField, validators, ValidationError
from sonar.models import db, User

class SignupForm(Form):
	firstname = TextField('First Name', [validators.Length(min=1, max=100)])
	lastname = TextField('Last Name', [validators.Length(min=1, max=100)])
	email = TextField('E-Mail Address', [validators.Length(min=1, max=120)])
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
	email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.Required("Please enter a password.")])

	def validate(self):
		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append("Invalid e-mail or password")
			return False