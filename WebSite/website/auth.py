from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests
from . import UserModel

auth = Blueprint('auth', __name__)
BASE = "http://127.0.0.1:5001/"

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_req = requests.get(BASE + "userDB/0?email=" + email)
        user_data = user_req.json()
        if 'password' in user_data:
            user_password = user_data['password']

        if user_req:
            if check_password_hash(user_password, password):
                flash('Logged in successfully!', category='success')
                if 'id' in user_data:
                    user_id = user_data['id']
                else:
                    return None
                if 'email' in user_data:
                    user_emai = user_data['email']
                if 'name' in user_data:
                    user_name = user_data['name']
                if 'age' in user_data:
                    user_age = user_data['age'] 
                if 'weight' in user_data:
                    user_weight = user_data['weight']
                user = UserModel(
                                id=user_id, 
                                email=user_emai, 
                                password=user_password, 
                                name=user_name, 
                                age=user_age, 
                                weight=user_weight)
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
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        age = request.form.get('age')
        weight = request.form.get('weight')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = requests.get(BASE + "userDB/0?email=" + email)
 
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = {"email" : email, "password" : generate_password_hash(
                password1, method='pbkdf2:sha256'), "name" : first_name, "age" : age, "weight" : weight}
            user_data = requests.put(BASE + "userDB/0", new_user).json()
            pr_user = UserModel(
                        id=user_data['id'], 
                         email=user_data['email'], 
                         password=user_data['password'],
                         name=user_data['name'],
                         age=user_data['age'],
                         weight=user_data['weight'])
            login_user(pr_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
