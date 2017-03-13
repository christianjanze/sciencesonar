from sonar import app
from flask import flash, render_template, request, url_for, redirect
from sonar.forms import LoginForm, RegistrationForm
from sonar.models import db

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User(form.email.data, form.password.data)
		db_session.add(user)
		flash('Thank you for registering')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)

	if request.method == 'POST' and form.validate():
		username = form.email.data
		password = form.password.data
		flash('Thank you for logging in', 'success')
		return redirect(url_for('index'))
	else:
		return render_template('login.html', form=form)

@app.route("/logout")
def logout():
	return render_template('logout.html')

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/discover")
def discover():
	return render_template('discover.html')

@app.route("/share")
def share():
	return render_template('share.html')

@app.route("/about")
def about():
	return render_template('about.html')

@app.route('/testdb')
def testdb():
	if db.session.query("1").from_statement("SELECT 1").all():
		return 'It works.'
	else:
		return 'Something is broken.'