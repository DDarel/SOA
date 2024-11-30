from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json
import requests

views = Blueprint('views', __name__)
BASE_USER = "http://127.0.0.1:5001/"
BASE_CALC = "http://127.0.0.1:5002/"



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        age = request.form.get('age')
        weight = request.form.get('weight')
        response = requests.patch(BASE_USER + "userDB/" + str(current_user.id), json={"age" : age, "weight" : weight})
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
    response = requests.delete(BASE_USER + "userDB/" + str(current_user.id))
    return redirect(url_for('auth.logout'))
