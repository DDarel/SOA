from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, UserMixin
import requests

db = None

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    db = SQLAlchemy(app)
    from .views import views
    from .auth import auth
    
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
        
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        user_data = UserModel.query.filter_by(id=user_id).first().json()
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


 

