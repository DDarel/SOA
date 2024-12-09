from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json
import requests
from . import UserModel
from . import db
views = Blueprint('views', __name__)
BASE_CALC = "http://127.0.0.1:5002/"



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        age = request.form.get('age')
        weight = request.form.get('weight')
        user = UserModel.query.filter_by(user_id=current_user.id).first()
        if user:
            user.user_age = age
            user.user_weight = weight
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template("home.html", user=current_user)

@views.route('/calculate_water', methods=['POST'])
@login_required
def calculate():
    if request.method == 'POST': 
        response = requests.get(BASE_CALC + "calculate/" + str(current_user.id) + "/" + str(current_user.weight))
        data_json = response.json()
        water = float(data_json['water'])
    return jsonify({"result": water})

@views.route('/delete_acc', methods=['POST'])
@login_required
def delete_acc(): 
    user = UserModel.query.filter_by(user_id=current_user.id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth.logout'))
