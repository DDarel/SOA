from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests
from . import UserModel
from . import db

auth = Blueprint('auth', __name__)

class UserModel(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        email = db.Column(db.String(100), nullable=False)
        password = db.Column(db.String(100), nullable=False)
        name = db.Column(db.String(100), nullable=False)
        age = db.Column(db.Integer, nullable=False)
        weight = db.Column(db.Float, nullable=False)
        
        def json(self):
            return {
                "id": self.id,
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "age": self.age,
                "weight": self.weight,
            }


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form.get('email')
        password = request.form.get('password')
        
        user_req = UserModel.query.filter_by(email=user_email).first()
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
        user_email = request.form.get('email')
        first_name = request.form.get('firstName')
        age = request.form.get('age')
        weight = request.form.get('weight')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = UserModel.query.filter_by(email=user_email).first()
 
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
                         email=user_email, 
                         password=password1,
                         name=first_name,
                         age=age,
                         weight=weight)
            db.session.add(pr_user)
            db.session.commit()
            login_user(pr_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
