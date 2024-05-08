from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from gp import db
from gp.models import Doctor, Patient ,ScanRequest,PatientInfo
from gp.doctors.forms import RegistrationForm,LoginForm,SubmitRequestForm
from gp.doctors.picture_handler import add_profile_pic

doctors = Blueprint('doctors',__name__)

# register
@doctors.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = Doctor(email=form.email.data,
                      username=form.username.data,
                      password=form.password.data,
                      specialization=form.specialization.data,)  # Adding specialization

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('doctors.login'))

    return render_template('register.html', form=form)




# login
@doctors.route('/login',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = Doctor.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')

            if next ==None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html',form=form)
# logout
@doctors.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@doctors.route("/request_list")
@login_required
def request_list():
    requests = db.session.query(ScanRequest, PatientInfo).join(PatientInfo, ScanRequest.patient_id == PatientInfo.patient_id).filter(ScanRequest.requests == False).all()
    forms = {request.ScanRequest.id: SubmitRequestForm() for request in requests}
    return render_template("request_list.html", requests=requests, forms=forms)




