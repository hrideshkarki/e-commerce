from flask import Blueprint, flash, redirect, render_template, request, url_for
from .models import User
from flask_login import current_user,login_user, logout_user, login_required
from app import app
from werkzeug.security import generate_password_hash
from .forms import  EditProfile

import requests as r
from flask import jsonify

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/profile', methods = ["GET", "POST"])
def profile():
    return render_template('profile.html')

@app.route('/edit-profile', methods = ["GET", "POST"])
def edit_profile():
    user = current_user
    form = EditProfile()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.password = generate_password_hash(password)
            user.save_changes()

            flash("Succesfully updated profile.", 'success')
            return redirect(url_for('profile'))
        else:
            flash('Invalid input. Please try again.', 'danger')
            return render_template('edit-profile.html', form = form)
        
    elif request.method == "GET":
        return render_template('edit-profile.html', form = form)
    
# @app.route('/api/<string:product_name>')
# def get_product_info(product_name):
#     # Your code to retrieve product info from the Genius API goes here
#     response = r.get('https://api.genius.com/search', headers={'Authorization': 'Bearer PRODUCT_API_KEY'}, params={'q': product_name})
#     product_info = response.json()
    
#     # instead of data = response.json()
#     print(jsonify(product_info))
#     return jsonify(product_info)


import requests as r
#import os
import json
#PRODUCT_API_KEY = os.environ.get('NEWS_API_KEY')

@app.route('/products')
def products_page():
    # note at end of this we add the pageSize=20
    
    params = {
        'api_key': 'C8FA965A8F6D4DDCB9FAC8BC1A5A2B52',
        'type': 'product',
        'asin': 'B000YDDF6O',
        'amazon_domain': 'amazon.com'
    }


    # make the http GET request to Rainforest API
    api_result = r.get('https://api.rainforestapi.com/request', params)

    # print the JSON response from Rainforest API
    print(json.dumps(api_result.json()))

    data = api_result.json()

    products = []
    # in the JSON it says that status should be 'ok', written in the JSON file
    if data['request_info']['success'] == 'true':
        products = data['product']['title']
        print(f"THE PRODUCTS ARE:{products}")

    return render_template('products.html', products=products)


