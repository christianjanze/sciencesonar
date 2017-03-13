from sonar import app
from flask import flash, render_template, request, url_for, redirect, session
from sonar.forms import SignupForm, SigninForm
from sonar.models import db, User

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	
	#If already logged in redirect to profile
	if 'email' in session:
		flash("You are already logged in. Please sign out before creating a new account.","danger")
		return redirect(url_for('profile'))

	if request.method == 'POST' and form.validate():
		newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
		db.session.add(newuser)
		db.session.commit()
		session['email'] = newuser.email
		
		flash("Welcome! You've successfully created your ScienceSonar account.", "success")

		return redirect(url_for('profile'))

	elif request.method == 'POST' and not form.validate(): 
		flash("Oops... Something went wrong", "danger")
		return render_template('signup.html', form=form)

	else:
		return render_template('signup.html', form=form)

@app.route('/profile')
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))
		
	user = User.query.filter_by(email = session['email']).first()
 
	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()

	#If already logged in redirect to profile
	if 'email' in session:
		flash("You are already logged in. Please sign out before signing in.","danger")
		return redirect(url_for('profile')) 

	if request.method == 'POST' and form.validate():
		flash("Welcome back on ScienceSonar", "success")
		session['email'] = form.email.data
		return redirect(url_for('profile'))

	elif request.method == 'POST' and not form.validate():
		flash("Error logging in. Please try again.", "danger")
		return render_template('signin.html', form=form)			 
	
	else:
		return render_template('signin.html', form=form)

@app.route('/signout')
def signout():

	if 'email' not in session:
		return redirect(url_for('signin'))

	flash("See you! Successfully logged out.","success")
	session.pop('email', None)
	return redirect(url_for('index'))


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