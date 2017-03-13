from wtforms import Form, BooleanField, TextField, StringField, PasswordField, validators

class RegistrationForm(Form):
	firstname = StringField('First Name', [validators.Length(min=1, max=50)])
	lastname = StringField('Last Name', [validators.Length(min=1, max=50)])
	email = StringField('E-Mail Address', [validators.Length(min=6, max=35)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords must match')
	])
	confirm = PasswordField('Password Confirmation')
	accept_tos = BooleanField('I accept the Terms of Service', [validators.DataRequired()])

class LoginForm(Form):
	email = StringField('E-Mail Address', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])