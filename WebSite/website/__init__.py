from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, UserMixin
import requests

BASE = "http://127.0.0.1:5001/"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        user_data = requests.get(BASE + "userDB/" + id).json()
        if 'id' in user_data:
            user_id = user_data['id']
        else:
            return None
        if 'email' in user_data:
            user_emai = user_data['email']
        if 'password' in user_data:
            user_password = user_data['password']
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
        return user
    
    return app

class UserModel(SQLAlchemy().Model, UserMixin):
	id = SQLAlchemy().Column(SQLAlchemy().Integer, primary_key=True)
	email = SQLAlchemy().Column(SQLAlchemy().String(100), nullable=False)
	password = SQLAlchemy().Column(SQLAlchemy().String(100), nullable=False)
	name = SQLAlchemy().Column(SQLAlchemy().String(100), nullable=False)
	age = SQLAlchemy().Column(SQLAlchemy().Integer)
	weight = SQLAlchemy().Column(SQLAlchemy().Float)
 

