from flask import render_template, Blueprint

core = Blueprint('core', __name__)

@core.route('/')
def index():
    return render_template('index.html')


@core.route('/info')
def info():
    #! crate info.html file
    return render_template('info.html')


@core.route('/support')
def support():
    return render_template('support.html')


@core.route('/tremsofuser')
def tremsofuser():
    return render_template('tremsofuser.html')