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
    patient_request = db.relationship('ScanRequest', backref='patient_info', lazy=True)

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
    patient_scan = db.relationship('ScanRequest', backref='doctor', lazy=True)

    def __init__(self, email, username, password, specialization):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.specialization = specialization

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.email}"
    
class ScanRequest(db.Model):
    __tablename__ = "scan_requests"  # Ensure table names are lowercase and snake_case for consistency
    id = db.Column(db.Integer, primary_key=True)
    scan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    patient_id = db.Column(db.String(32), db.ForeignKey('patient_info.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    requests = db.Column(db.Boolean, default=False, nullable=False)  # Boolean column with default False

    def __init__(self, patient_id, doctor_id, requests=False):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.scan_date = datetime.utcnow()  # Optionally allow passing this as a parameter if needed
        self.requests = requests  # Initialize with the provided value or default to False

    def __repr__(self):
        return f"<ScanRequest(id={self.id}, scan_date={self.scan_date}, patient_id={self.patient_id}, doctor_id={self.doctor_id}, requests={self.requests})>"



