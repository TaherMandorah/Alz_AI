from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from gp import db
from gp.models import Doctor, Patient,ScanRequest,PatientInfo
from gp.patients.forms import AddPatientForm, SearchAddPatientForm, UpdateUserForm,ToProfileForm,ToResultForm,PatientInfoForm,RequestSearchForm,RequestForm
from gp.patients.picture_handler import add_profile_pic
from datetime import datetime
import pytz

def get_ksa_time():
    utc_time = datetime.utcnow()
    ksa_timezone = pytz.timezone('Asia/Riyadh')
    ksa_time = utc_time.replace(tzinfo=pytz.utc).astimezone(ksa_timezone)
    return ksa_time

patients = Blueprint("patients", __name__)


@patients.route("/add_patient", methods=["GET", "POST"])
@login_required
def add_patient():
    form = AddPatientForm()
    patient_id = request.args.get('patient_id', None)
    request_id = request.args.get('request_id', None)  # Get the request_id from query parameters

    if patient_id:
        form.patient_id.data = patient_id
        form.patient_id.render_kw = {'readonly': True}

    if form.validate_on_submit():
        if form.brain_img.data:
            patient_info = PatientInfo.query.filter_by(patient_id=form.patient_id.data).first()
            if not patient_info:
                flash('No existing patient info found for this ID.', 'warning')
                return render_template("add_patient.html", form=form)

            pic = add_profile_pic(form.brain_img.data, form.patient_id.data)
            patient = Patient(
                patient_id=form.patient_id.data,
                brain_img=pic,
                date=get_ksa_time(),  # Adjusted to KSA time
                classifier="gg",
                accuracy=69.69,
                doctor_id=current_user.id
            )
            db.session.add(patient)

            # Update the scan request status if a request_id was provided
            if request_id:
                scan_request = ScanRequest.query.get(int(request_id))
                if scan_request:
                    scan_request.requests = True
                    db.session.commit()
                    flash('Scan added and request marked as completed.', 'success')
                else:
                    flash('No matching scan request found.', 'error')

            return redirect(url_for("patients.result", username_id=form.patient_id.data, pic=pic))
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
            # new_scan = ScanRequest(
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
        return redirect(url_for("patients.profile", username_id=username_id))
    return render_template("search_patient.html", form=form)


@patients.route("/profile/<username_id>", methods=["GET", "POST"])
@login_required
def profile(username_id):
    # Query the PatientInfo based on patient_id
    patient_info = PatientInfo.query.filter_by(patient_id=username_id).first()
    if not patient_info:
        flash("No patient information available.")
        return redirect(url_for("patients.add_patient_info"))

    # Query all related Patient records and order them by date in ascending order
    patients = Patient.query.filter_by(patient_id=username_id).order_by(Patient.date.desc()).all()
    if not patients:
        flash("No scans found for this patient.")
        return redirect(url_for("patients.add_patient")) 

    # Create a map of doctors for each patient
    doctor_map = {patient.id: Doctor.query.get(patient.doctor_id) for patient in patients if patient.doctor_id}

    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.brain_img.data:
            pic = add_profile_pic(form.brain_img.data, username_id)
            for patient in patients:
                patient.brain_img = pic
        if patient_info:
            patient_info.username = form.username.data
        db.session.commit()
        flash("Profile Updated Successfully!")
        return redirect(url_for("patients.profile", username_id=username_id))

    elif request.method == "GET" and patient_info:
        form.username.data = patient_info.username

    form2 = ToResultForm()
    if form2.validate_on_submit():
        return redirect(url_for("patients.result", username_id=username_id))
    
    return render_template("profile.html", patient_info=patient_info, patients=patients, doctor_map=doctor_map, form=form, form2=form2)




@patients.route("/result/<username_id>", methods=["GET", "POST"])
@login_required
def result(username_id):
    pic = request.args.get('pic', None)  # Get pic parameter from query string

    # Query for the latest patient record based on the 'date' field
    patient = Patient.query.filter_by(patient_id=username_id).order_by(Patient.date.desc()).first()
    if not patient:
        flash("No patient found with the given ID.", "warning")
        return redirect(url_for("patients.add_patient"))

    # Continue with the rest of the existing code
    doctor = Doctor.query.filter_by(id=patient.doctor_id).first()
    patient_info = PatientInfo.query.filter_by(patient_id=username_id).first()
    if not patient_info:
        flash("No personal information found for this patient.", "warning")
        return redirect(url_for("patients.add_patient_info"))

    form = ToProfileForm()
    if form.validate_on_submit():
        return redirect(url_for("patients.profile", username_id=username_id))

    # Pass both patient and patient_info objects to the template, along with the pic
    return render_template("results.html", patient=patient, doctor=doctor, patient_info=patient_info, pic=pic, form=form)



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
        return redirect(url_for("patients.request_scan"))
    else:
        print("form is not working properly")
    return render_template("patient_info.html", form=form)

@patients.route("/request", methods=["GET", "POST"])
@login_required
def request_scan():
    search_form = RequestSearchForm()
    request_form = RequestForm()

    if search_form.validate_on_submit() and search_form.submit.data:
        patient_info = PatientInfo.query.filter_by(patient_id=search_form.patient_id.data).first()
        if patient_info:
            return redirect(url_for("patients.request_scan", patient_id=patient_info.patient_id))  # Pass patient_id as query parameter
        else:
            flash("No patient found with this ID.", "warning")

    # Checking if 'patient_id' is in query string for continuity in form submissions
    patient_id = request.args.get('patient_id')
    if patient_id:
        patient_info = PatientInfo.query.filter_by(patient_id=patient_id).first()
        if request_form.validate_on_submit() and request_form.submit.data:
            if patient_info:
                new_request = ScanRequest(patient_id=patient_info.patient_id, doctor_id=current_user.id)
                db.session.add(new_request)
                db.session.commit()
                flash("Scan request submitted successfully.", "success")
                return redirect(url_for("patients.request_scan"))
            else:
                flash("Failed to submit request. Patient not found.", "error")
        return render_template("request_scan.html", search_form=search_form, request_form=request_form, patient_info=patient_info)
    
    return render_template("request_scan.html", search_form=search_form, request_form=request_form)
