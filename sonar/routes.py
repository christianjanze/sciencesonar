from sonar import app
from flask import flash, render_template, request, url_for, redirect, session
from sonar.forms import SignupForm, SigninForm, IdeaForm, DatasetForm
from sonar.models import db, User, Idea, Dataset
from werkzeug.utils import secure_filename
import os
import calendar
import datetime

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
	form = SignupForm()
	
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


@app.route('/idea', methods=['GET', 'POST'])
def idea():
	#Check if user is signed in
	if 'email' not in session:
		flash("You must be signed in to post an idea.")
		return redirect(url_for('signin'))
		
	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		flash("You must be signed in to post an idea.")
		return redirect(url_for('signin'))

	#if user is signed in...
	form = IdeaForm()

	if request.method == 'POST' and form.validate():
		
		newidea = Idea(form.title.data, form.description.data, user.uid)
		db.session.add(newidea)
		db.session.commit()
		
		flash("Thank you for creating the new idea", "success")

		return redirect(url_for('profile'))

	elif request.method == 'POST' and not form.validate(): 

		flash_errors(form) # TODO: REMOVE LINE IN PRODUCTION
		flash("Oops... Something went wrong", "danger")
		return render_template('idea.html', form=form)

	else:
		return render_template('idea.html', form=form)


@app.route('/dataset', methods=['GET', 'POST'])
def dataset():

	#Check if user is signed in
	if 'email' not in session:
		flash("You must be signed in to upload a dataset.")
		return redirect(url_for('signin'))
		
	user = User.query.filter_by(email = session['email']).first()

	if user is None:
		flash("You must be signed in to upload a dataset")
		return redirect(url_for('signin'))

	#if user is signed in...
	form = DatasetForm()
	if request.method == 'POST' and form.validate():
		f = form.dataset.data
		filename = secure_filename(f.filename)

		d = datetime.datetime.utcnow()
		unixtime = calendar.timegm(d.utctimetuple())

		filename_disk = str(user.uid) + "_" + str(unixtime) +"_"+ filename

		f.save(os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']+filename_disk)))

		filesize_bytes = os.stat(os.path.join(app.config['UPLOAD_FOLDER'], filename_disk)).st_size


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

	else:
		return render_template('dataset.html', form=form)


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