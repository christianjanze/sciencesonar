from flask import Flask
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24) # Set random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sonar_user:sonar_password@localhost/development' #conda install pymysql first

from sonar.models import db
db.init_app(app)

import sonar.routes