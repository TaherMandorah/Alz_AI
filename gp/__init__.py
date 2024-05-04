from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager

app = Flask(__name__)
app.app_context().push()

app.config["SECRET_KEY"] = "MY_SECRET_KEY"
app.config["UPLOAD_FOLDER"] = current_app.root_path + "/static/profile_pics/"




################################################################
basdir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basdir, "database.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)
##################################################################
#! Login CONFIGURATION
login_manager = LoginManager(app)
login_manager.init_app(app)

login_manager.login_view = "doctors.login"




from gp.core.views import core
from gp.error_pages.handlers import error_pages
from gp.doctors.views import doctors
from gp.patients.views import patients

app.register_blueprint(doctors)
app.register_blueprint(error_pages)
app.register_blueprint(core)
app.register_blueprint(patients)
