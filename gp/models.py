from gp import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return Doctor.query.get(int(user_id))


class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(32), db.ForeignKey('patient_info.patient_id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    brain_img = db.Column(db.String(64), nullable=False)
    classifier = db.Column(db.String(32))
    accuracy = db.Column(db.Float)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))

    def __init__(self, patient_id, brain_img, classifier, accuracy, doctor_id, date):
        self.patient_id = patient_id
        self.brain_img = brain_img
        self.classifier = classifier
        self.accuracy = accuracy
        self.doctor_id = doctor_id
        self.date = date

    def __repr__(self):
        return f"<Patient {self.id} - {self.patient_id}>"


class PatientInfo(db.Model):
    __tablename__ = "patient_info"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    patient_id = db.Column(db.String(32), unique=True, index=True)
    age = db.Column(db.String(32))
    gender = db.Column(db.String(32))

    # Relationship: One PatientInfo to many Patients
    patients = db.relationship('Patient', backref='patient_info', lazy=True)

    def __init__(self, username, patient_id, gender, age):
        self.username = username
        self.patient_id = patient_id
        self.gender = gender
        self.age = age

    def __repr__(self):
        return f"<PatientInfo {self.username}>"

class Doctor(db.Model, UserMixin):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    specialization = db.Column(db.String(64))

    # Define the one-to-many relationship
    patients = db.relationship('Patient', backref='doctor', lazy=True)

    def __init__(self, email, username, password, specialization):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.specialization = specialization

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.email}"
    
class ScanHistory(db.Model):
    __tablename__ = "scan_history"
    id = db.Column(db.Integer, primary_key=True)
    scan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    doctor_name = db.Column(db.String(64), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    

    def __init__(self, doctor_name, result, patient_id):
        self.doctor_name = doctor_name
        self.result = result
        self.patient_id = patient_id

    def __repr__(self):
        return f"Scan History: {self.scan_date}, Doctor: {self.doctor_name}, Result: {self.result}"


