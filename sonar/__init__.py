from flask import Flask
#import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key_change_before" #os.urandom(24) # Set random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sonar_user:sonar_password@localhost/development' 

from sonar.models import db
db.init_app(app)

import sonar.routes