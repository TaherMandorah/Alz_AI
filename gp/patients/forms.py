from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms import StringField, DateTimeField,SubmitField,SelectField,FloatField,IntegerField
from wtforms.validators import ValidationError
from flask_wtf.file import FileField, FileAllowed


class AddPatientForm(FlaskForm):
    patient_id = StringField("Patient ID:", validators=[DataRequired()])
    brain_img = FileField("Choose a file", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Submit")
    
                # Patient class from models.py
                # id = db.Column(db.Integer, primary_key=True)
                # patient_id = db.Column(db.String(32), db.ForeignKey('patient_info.patient_id'), nullable=False)
                # date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
                # brain_img = db.Column(db.String(64), nullable=False)
                # classifier = db.Column(db.String(32))
                # accuracy = db.Column(db.Float)
                # doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))

class SearchAddPatientForm(FlaskForm):
    patient_id = StringField("Patient ID:", validators=[DataRequired()])
    submit = SubmitField("Search Patient")


class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    patient_id = StringField("Patient ID:", validators=[DataRequired()])
    brain_img = FileField('Choose a file', validators=[FileAllowed(['png', 'jpg',])])
    submit = SubmitField('Update')

class ToProfileForm(FlaskForm):
    submit = SubmitField('Profile')

class ToResultForm(FlaskForm):
    submit = SubmitField('Result')
    
class PatientInfoForm(FlaskForm):
    username = StringField("Patient Name: ", validators=[DataRequired()])
    patient_id = StringField("Patient ID: ", validators=[DataRequired()])
    gender = SelectField('gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    age = StringField("Age:", validators=[DataRequired()])
    submit = SubmitField("GG")