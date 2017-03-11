from flask import Flask, render_template
app = Flask(__name__)

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


@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/logout")
def logout():
	return render_template('logout.html')

if __name__ == "__main__":
    app.run(debug=True) #remove debug=True in production