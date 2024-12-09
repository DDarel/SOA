from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, UserMixin
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask_user:004039Vlad@user-database.cn8m0yeugq4j.eu-central-1.rds.amazonaws.com:5432/user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserModel(db.Model):
        __tablename__ = 'users'
        user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        user_email = db.Column(db.String(100), nullable=False)
        user_password = db.Column(db.String(100), nullable=False)
        user_name = db.Column(db.String(100), nullable=False)
        user_age = db.Column(db.Integer, nullable=False)
        user_weight = db.Column(db.Float, nullable=False)
        
        def json(self):
            return {
                "id": self.user_id,
                "name": self.user_name,
                "email": self.user_email,
                "password": self.user_password,
                "age": self.user_age,
                "weight": self.user_weight,
            }

def create_app():
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        user_data = UserModel.query.filter_by(user_id=id).first().json()
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


 

