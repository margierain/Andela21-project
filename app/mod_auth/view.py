from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from app import db
from app.mod_auth.forms import LoginForm
from app.mod_auth.model import User
# define the blueprints
mod_auth = Blueprint('auth',__name__, url_prefix='/auth')
#
@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form) 
    if  form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.user_id
            flash('Welcome %s' % user.name)
            return redirect(url_for('auth.')) # needs correction.
        flash('Incorrect password or email')    
    return render_template('auth/login.html', form=form)  
                
