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

class UserModel(db.Model, UserMixin):
        __tablename__ = 'users'
        user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        user_email = db.Column(db.String(100), nullable=False)
        user_password = db.Column(db.String(100), nullable=False)
        user_name = db.Column(db.String(100), nullable=False)
        user_age = db.Column(db.Integer, nullable=False)
        user_weight = db.Column(db.Float, nullable=False)
        
        def get_id(self):
            return str(self.user_id)
    
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
    def load_user(user_id):
        return UserModel.query.get(int(user_id))
    
    return app


 

