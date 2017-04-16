from flask_wtf import Form
from flask import  flash
from wtforms import BooleanField, StringField, PasswordField, validators, ValidationError,SelectMultipleField
from wtforms.widgets import TextArea
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileRequired
from sonar.models import User, Tag, Scientificfield
from sonar import db
import re
import sys #Tempß

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
	

def tag_choices():      
	return Tag.query # db.session.query(Tag).all()

def scientificfield_choices():
	return Scientificfield.query

class Select2MultipleField(QuerySelectField):
 	def pre_validate(self, form):
 	 # Prevent "not a valid choice" error
 		pass
 	def process_formdata(self, valuelist):
 		if valuelist:
 			self.data = valuelist
 		else:
 			self.data = ""

class IdeaForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=100)])
	question = StringField('Research Question', [validators.Length(min=1, max=100)])
	description = StringField('Description', [validators.Length(min=1, max=10000)], widget=TextArea())
	scientificfield = QuerySelectField('Scientific Field', query_factory=scientificfield_choices, get_label='description')
	tags = Select2MultipleField('Tags', 
			query_factory=tag_choices,
			get_label='description',
			render_kw={"multiple": "multiple", "data-tags": "1"})

class DatasetForm(Form):
	title = StringField('Title', [validators.Length(min=1, max=100)])
	description = StringField('Description', widget=TextArea())
	dataset = FileField(validators=[FileRequired()])