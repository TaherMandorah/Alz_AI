from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from gp import db
from gp.models import Doctor, Patient,ScanHistory,PatientInfo
from gp.patients.forms import AddPatientForm, SearchAddPatientForm, UpdateUserForm,ToProfileForm,ToResultForm,PatientInfoForm
from gp.patients.picture_handler import add_profile_pic
from datetime import datetime


patients = Blueprint("patients", __name__)


@patients.route("/patient", methods=["GET", "POST"])
@login_required
def add_patient():
    form = AddPatientForm()
    if form.validate_on_submit():
        if form.brain_img.data:
            pic = add_profile_pic(form.brain_img.data, form.patient_id.data)

            # Ensure that the date from the form is correctly formatted or processed
            # If your form outputs a datetime object, you don't need to parse it again
            # But if you need to adjust or ensure no second/microsecond data, you can use:
            patient = Patient(
                patient_id=form.patient_id.data,
                brain_img=pic,
                date= datetime.utcnow(),
                classifier="classi",
                accuracy=99.88,
                doctor_id=current_user.id  # Assuming current_user.id is correctly used
            )

            db.session.add(patient)
            db.session.commit()
            flash('Patient added successfully!', 'success')
            return redirect(url_for("patients.result", username_id=form.patient_id.data))
        
        else:
            flash('Error: Image file is required.', 'danger')

    return render_template("add_patient.html", form=form)
            ####################################################
                # AddPatientForm from forms.py
                
                # patient_id = StringField("Patient ID:", validators=[DataRequired()])
                # brain_img = FileField("Choose a file", validators=[FileAllowed(["jpg", "png"])])
                # date = DateTimeField("Date of Scan", format='%Y-%m-%d %H:%M', validators=[DataRequired()], render_kw={"placeholder": "Format: YYYY-MM-DD HH:MM"})
                # classifier = StringField("Classification :", validators=[DataRequired()])
                # accuracy = FloatField("Accuracy of Analysis (%)", validators=[DataRequired()])
                # doctor_id = IntegerField("Doctor ID:", validators=[DataRequired()], render_kw={'readonly': True})
                # submit = SubmitField("Submit")
                
            #########################################################
            # Add a new scan record to the scan history
            # new_scan = ScanHistory(
            #     doctor_name=current_user.username,  # Assuming current user is the doctor adding the patient
            #     result="Initial scan result",
            #     patient_id=patient.id
            # )
            # db.session.add(new_scan)
            # db.session.commit()
@patients.route("/search_patient", methods=["GET", "POST"])
@login_required
def search_patient():
    form = SearchAddPatientForm()
    if form.validate_on_submit():
        username_id = form.patient_id.data
        return redirect(url_for("patients.result", username_id=username_id))
    return render_template("search_patient.html", form=form)


@patients.route("/profile/<username_id>", methods=["GET", "POST"])
@login_required
def profile(username_id):
    patient = Patient.query.filter_by(patient_id=username_id).first()
    scan_history = ScanHistory.query.filter_by(patient_id=patient.id).all()
    form = UpdateUserForm()
    
    if form.validate_on_submit():
        if form.brain_img.data:
            # Check if name is updated correctly
            print(f"Updated name: {form.username.data}")
            # Check if add_profile_pic returns a path
            print(f"Uploaded picture path:")
            username_ = patient.patient_id
            pic = add_profile_pic(form.brain_img.data, username_)
            patient.brain_img = pic
        patient.username = form.username.data
        db.session.commit()
        flash("Profile Updated Successfully!")
        return redirect(url_for("patients.profile", username_id=username_id))
    elif request.method == "GET":
        form.username.data = patient.username
        form.patient_id.data = patient.patient_id

    form2 = ToResultForm()
    if form2.validate_on_submit():
        return redirect(url_for("patients.result", username_id=username_id))
    
    return render_template("profile.html", patient=patient, form=form, scan_history=scan_history , form2=form2)


@patients.route("/result/<username_id>", methods=["GET", "POST"])
@login_required
def result(username_id):
    
    patient = Patient.query.filter_by(patient_id=username_id).first()
    doctor = Doctor.query.filter_by(id=patient.doctor_id).first()
    form = ToProfileForm()
    if form.validate_on_submit():
        return redirect(url_for("patients.profile", username_id=username_id))
    return render_template("results.html", patient=patient,doctor=doctor, form=form)


@patients.route("/patient_info", methods=["GET", "POST"])
@login_required
def patient_info():
    form = PatientInfoForm()
    if form.validate_on_submit():
        print("hello")
        patient_info = PatientInfo(
            username=form.username.data,
            patient_id=form.patient_id.data,
            gender=form.gender.data,
            age=form.age.data
            # PatientInfoForm from forms.py
            # username = StringField("Patient Name: ", validators=[DataRequired()])
            # patient_id = StringField("Patient ID: ", validators=[DataRequired()])
            # gender = SelectField('gender', choices=[('Male', 'Male'), ('Female', 'Female')])
            # age = StringField("Age:", validators=[DataRequired()])
        )
        db.session.add(patient_info)
        db.session.commit()
        return redirect(url_for("patients.search_patient"))
    else:
        print("form is not working properly")
    return render_template("patient_info.html", form=form)