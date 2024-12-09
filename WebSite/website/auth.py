from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests
from . import UserModel
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form.get('email')
        password = request.form.get('password')
        
        user_req = UserModel.query.filter_by(user_email=user_email).first()
        if user_req is not None:
            user_password = user_req.user_password

        if user_req:
            if check_password_hash(user_password, password):
                flash('Logged in successfully!', category='success')
                user_id = user_req.user_id
                user_email = user_req.user_email
                user_name = user_req.user_name
                user_age = user_req.user_age
                user_weight = user_req.user_weight
                user = UserModel(
                                user_id=user_id, 
                                user_email=user_email, 
                                user_password=user_password, 
                                user_name=user_name, 
                                user_age=user_age, 
                                user_weight=user_weight)
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user_email = request.form.get('email')
        first_name = request.form.get('firstName')
        age = request.form.get('age')
        weight = request.form.get('weight')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = UserModel.query.filter_by(user_email=user_email).first()
 
        if user:
            flash('Email already exists.', category='error')
        elif len(user_email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # new_user = {"email" : user_email, "password" : generate_password_hash(
            #     password1, method='pbkdf2:sha256'), "name" : first_name, "age" : age, "weight" : weight}
            # user_data = requests.put(BASE + "userDB/0", json=new_user).json()
            pr_user = UserModel( 
                         user_email=user_email, 
                         user_password=generate_password_hash(password1, method='pbkdf2:sha256'),
                         user_name=first_name,
                         user_age=age,
                         user_weight=weight)
            db.session.add(pr_user)
            db.session.commit()
            login_user(pr_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
