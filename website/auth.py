from website.models import User
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged In Successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, Please Try Again.', category='error')
        else:
            flash('Email Does Not Exist.', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('This Email Is Already Exists.', category='error')
        elif len(name) < 3:
            flash('Name Must Be Have 3 Character', category='error')
        elif len(email) < 7:
            flash('Email Must Be Have 7 Character', category='error')
        elif len(password1) < 5:
            flash('Password Must Be Have 5 Character', category='error')
        elif password1 != password2:
            flash('Password Does\'t Match.', category='error')
        else:
            #Store to the database.
            new_user = User(name=name, email=email, password=generate_password_hash
            (password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Was Successfully Created', category='success')
            
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)