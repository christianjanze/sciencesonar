from functools import wraps
from sonar import app
from flask import flash, render_template, request, url_for, redirect, session, g
from sonar.forms import SignupForm, SigninForm, IdeaForm, DatasetForm
from sonar.models import User, Idea, Dataset, Tag
from sonar import login_manager, db
from werkzeug.utils import secure_filename
import os, calendar, datetime
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug import generate_password_hash
from sqlalchemy.orm import joinedload
import sys
import datetime

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

# Auxiliary function to generate flash messages from errors in forms
def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash("Error in the %s field - %s" % (
				getattr(form, field).label.text,
				error
			))

@app.route('/signup', methods=['GET', 'POST'])
def signup():	
	if g.user.is_authenticated:
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
	##ideas = Idea.query.filter_by(user_id=g.user.id)
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
		login_user(registered_user, remember=True)
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

@app.route('/dataset/new', methods=['GET', 'POST'])
@login_required
def dataset():
	form = DatasetForm()

	if request.method == 'POST' and form.validate():
		f = form.dataset.data
		filename = secure_filename(f.filename)

		#UNIX UTC timestanmp
		d = datetime.datetime.utcnow()
		unixtime = calendar.timegm(d.utctimetuple())

		filename_disk = str(g.user.id) + "_" + str(unixtime) +"_"+ filename
		f.save(os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']+filename_disk)))
		
		filesize_bytes = os.stat(os.path.join(app.config['UPLOAD_FOLDER'], filename_disk)).st_size

		license = "MIT" # TODO

		newdataset = Dataset(title=form.title.data, description=form.description.data, filename=filename, filename_disk=filename_disk, filesize_bytes=filesize_bytes, license=license)
		g.user.datasets.append(newdataset)

		db.session.add(g.user)
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
	return render_template('share.html')

@app.route("/")
def index():
	n_users = User.query.count()
	n_ideas= Idea.query.count()
	n_datasets = Dataset.query.count()
	#n_institutions # TODO: once possible to enter workplace, count number
	n_institutions = 2

	featured_ideas = db.session.query(Idea).filter(Idea.is_featured=="yes").options(joinedload(Idea.user), joinedload(Idea.tags), joinedload(Idea.scientificfield)).limit(3)
	return render_template('index.html',featured_ideas=featured_ideas,n_users=n_users,n_ideas=n_ideas,n_datasets=n_datasets,n_institutions=n_institutions)

@app.route("/discover")
def discover():
	n_ideas= Idea.query.count()
	n_datasets = Dataset.query.count()
	now = datetime.datetime.utcnow()

	ideas = db.session.query(Idea).options(joinedload(Idea.user), joinedload(Idea.tags), joinedload(Idea.scientificfield)).all()
	return render_template('discover.html', ideas=ideas, n_ideas=n_ideas, n_datasets=n_datasets,now=now)

@app.route("/about")
def about():
	return render_template('about.html')
	

@app.route('/idea/new', methods=['GET', 'POST'])
@login_required
def idea():
	form = IdeaForm()

	if request.method == 'POST' and form.validate():

		#TODO:
		#refactor part below (appears 1x above)
		#Handle existing and new tags
		# TODO: what happens if someone adds a new field with the same name at the same time before commit?
		# TODO: --> Check whether new tags were already added in the meantime
		# TODO: lowercase everything
		tag_ids = [] #stores all ids (existing and newly created ones)
		#Add new tags to tag table
		for tag in form.tags.data:
			#Handle new tags
			if tag.startswith("newtag_"):
				newtag = Tag(description=tag[7:])
				db.session.add(newtag)
				db.session.commit()
				tag_ids.append(newtag.id)
			#handle old tags
			else:
				tag_ids.append(tag)

		newidea = Idea(user_id=g.user.id, title=form.title.data, question=form.question.data, description=form.description.data, scientificfield_id=form.scientificfield.data.id)
		for tag_id in tag_ids:
		 	tag = Tag.query.get(tag_id)
		 	newidea.tags.append(tag)

		db.session.add(newidea)
		db.session.commit()

		flash("Thank you for creating the new idea", "success")

		return redirect(url_for('profile'))

	elif request.method == 'POST' and not form.validate(): 

		flash("Oops... Something went wrong", "danger")
		return render_template('idea_new.html', form=form)

	elif request.method =='GET':
		return render_template('idea_new.html', form=form)


@app.route('/idea/<int:idea_id>', methods=['GET'])
@login_required
def show_idea(idea_id):
	#idea=Idea.query.get(variable)
	now = datetime.datetime.utcnow()
	idea = db.session.query(Idea).filter(Idea.id==idea_id).options(joinedload(Idea.user), joinedload(Idea.tags), joinedload(Idea.datasets)).first()
	if idea:
		return render_template("idea_show.html",idea=idea,now=now)
	else:
		flash("Oops... Something went wrong", "danger")
		return redirect("/")

@app.route('/idea/<int:idea_id>/delete', methods=['GET'])
@login_required
def delete_idea(idea_id):
	idea = Idea.query.filter(Idea.user_id==g.user.id, Idea.id==idea_id).first()
	if idea:
		db.session.delete(idea)
		db.session.commit()
		flash("Successfully deleted idea", "success")
		return redirect("/")
	else:
		return render_template('404.html'), 404

@app.route('/idea/<int:idea_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_idea(idea_id):
	#Checks if idea exists and whether it belongs to the user
	idea= Idea.query.filter(Idea.user_id==g.user.id, Idea.id==idea_id).first()
	if idea:
		form=IdeaForm(obj=idea)
		if request.method=="POST" and form.validate():
			
			#TODO:
			#refactor part below (appears 1x above)
			tag_ids = [] 
			for tag in form.tags.data:
				#Handle new tags
				if tag.startswith("newtag_"):
					newtag = Tag(description=tag[7:])
					db.session.add(newtag)
					db.session.commit()
					tag_ids.append(newtag.id)
				#handle old tags
				else:
					tag_ids.append(tag)

			idea.tags=[] #remove existing tags
			for tag_id in tag_ids:
				tag = Tag.query.get(tag_id)
				idea.tags.append(tag)

			for tag in idea.tags:
				print(tag, file=sys.stderr)

			idea.title=form.title.data
			idea.question=form.question.data
			idea.description=form.description.data
			idea.scientificfield_id=form.scientificfield.data.id
			idea.updated_date = datetime.datetime.utcnow()

			db.session.add(idea)
			db.session.commit()

			flash("Successfully updated idea!", "success")

			return redirect(url_for('show_idea',idea_id=idea.id)) # go somewhere

		return render_template("idea_edit.html", form=form)
	else:
		return render_template('404.html'), 404