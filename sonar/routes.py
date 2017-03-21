from functools import wraps
from sonar import app
from flask import flash, render_template, request, url_for, redirect, session, g
from sonar.forms import SignupForm, SigninForm, IdeaForm, DatasetForm
from sonar.models import db, User, Idea, Dataset
from sonar import login_manager
from werkzeug.utils import secure_filename
import os, calendar, datetime
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from werkzeug import generate_password_hash

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user

# Auxiliary function to generate flash messages from errors in forms
def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(u"Error in the %s field - %s" % (
				getattr(form, field).label.text,
				error
			))

@app.route('/signup', methods=['GET', 'POST'])
def signup():	
	if user is not None:
		flash("You are already logged in. Please sign out before creating a new account.","danger")
		return redirect(url_for('profile'))

	form = SignupForm()

	if request.method == 'POST' and form.validate():
		newuser = User(form.firstname.data, form.lastname.data, form.username.data, form.password.data)
		db.session.add(newuser)
		db.session.commit()
		
		flash("Welcome! You've successfully created your ScienceSonar account.", "success")

		return redirect(url_for('signin'))

	elif request.method == 'POST' and not form.validate(): 
		flash("Oops... Something went wrong", "danger")
		return render_template('signup.html', form=form)

	else:
		return render_template('signup.html', form=form)

@app.route('/profile')
@login_required
def profile():
	return render_template('profile.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()

	if request.method == 'GET':
		return render_template('signin.html', form=form)

	username = form.username.data.lower()
	password = form.password.data

	registered_user = User.query.filter_by(username = username).first()

	if registered_user and registered_user.check_password(password):
		login_user(registered_user)
		flash("Logged in successfully", "success")
		return redirect(request.args.get('next') or url_for('profile'))
	else:
		flash('Username or Password is invalid' , 'error')
		return redirect(url_for('signin'))

@app.route('/signout')
@login_required
def signout():
	logout_user()
	flash("See you! Successfully logged out.","success")
	return redirect(url_for('index')) 

@app.route('/idea', methods=['GET', 'POST'])
@login_required
def idea():
	form = IdeaForm()

	if request.method == 'POST' and form.validate():
		
		newidea = Idea(form.title.data, form.description.data, g.user.id, form.scientific_area.data, form.scientific_subarea.data)
		db.session.add(newidea)
		db.session.commit()
		
		flash("Thank you for creating the new idea", "success")

		return redirect(url_for('profile'))

	elif request.method == 'POST' and not form.validate(): 

		flash_errors(form) # TODO: REMOVE LINE IN PRODUCTION
		flash("Oops... Something went wrong", "danger")
		return render_template('idea.html', form=form)

	elif request.method =='GET':

		return render_template('idea.html', form=form)


@app.route('/dataset', methods=['GET', 'POST'])
@login_required
def dataset():
	form = DatasetForm()

	if request.method == 'POST' and form.validate():
		f = form.dataset.data
		filename = secure_filename(f.filename)

		#Calc UNIX UTC timestanmp
		d = datetime.datetime.utcnow()
		unixtime = calendar.timegm(d.utctimetuple())

		#
		filename_disk = str(user.uid) + "_" + str(unixtime) +"_"+ filename
		f.save(os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']+filename_disk)))
		
		filesize_bytes = os.stat(os.path.join(app.config['UPLOAD_FOLDER'], filename_disk)).st_siz

		license = "MIT" # TODO

		newdataset = Dataset(form.description.data, filename, filename_disk, filesize_bytes, license, user.uid)

		db.session.add(newdataset)
		db.session.commit()
		
		flash("Thank you for uploading this dataset", "success")

		return redirect(url_for('profile'))

	elif request.method == 'POST' and not form.validate(): 
		flash_errors(form) # TODO: REMOVE LINE IN PRODUCTION
		flash("Oops... Something went wrong", "danger")
		return render_template('dataset.html', form=form)

	elif request.method == 'GET':
		return render_template('dataset.html', form=form)


@app.route("/share")
@login_required
def share():
	ideas = Idea.query.filter_by(user_id=g.user.id)
	return render_template('share.html',ideas=ideas)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/discover")
def discover():
	return render_template('discover.html')

@app.route("/about")
def about():
	return render_template('about.html')