from flask import Blueprint, flash, redirect, render_template, request, url_for
from .models import Product, User
from flask_login import current_user,login_user, logout_user, login_required
from app import app
from werkzeug.security import generate_password_hash
from .forms import AddProduct, EditProfile
import os
import requests as r
from flask import jsonify

PRODUCT_API_KEY = os.environ.get('PRODUCT_API_KEY')

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
    
#@app.route('/add-product/<string:ASIN>')
@app.route('/products')
def products_page():
    products = Product.query.all()
   
    return render_template('products.html', products=products)

@app.route('/product/<int:id>')
def single_product(id):
    # we need to query to find the product where the ID = the id
    product = Product.query.get(id)
    return render_template('single-product.html', p=product)

@app.route('/add-product/<string:ASIN>')
def add_product(ASIN):
    params = {
        'api_key': 'C8FA965A8F6D4DDCB9FAC8BC1A5A2B52',
        'type': 'product',
        'amazon_domain': 'amazon.com'
    }

    params['asin']= ASIN

    api_result = r.get('https://api.rainforestapi.com/request', params)
    
    data = api_result.json()

    if data["request_info"]["success"] == True:
        product = data["product"]

        title = product["title"]
        try:
            price = product["price"]["value"]
        except:
            price = product["buybox_winner"]["price"]["value"]
        image = product["main_image"]["link"]
        department = product["categories"][0]["name"]
        amazon_link = product["link"]
        try:
            description = product["description"]
        except:
            description = product["feature_bullets"]
        rating = product["rating"]

        new_product = Product(title, price, image, department, amazon_link, description, rating)
        new_product.save_to_db()
                                            # fix this, fix HTML
        return redirect (url_for('admin_add_product'))
    else:
        flash ('unable to add product', 'danger')
        return render_template('add-product.html')


@app.route('/add-product', methods = ["GET", "POST"])
def admin_add_product():
    form = AddProduct()
    if request.method == "POST":
        if form.validate():

            flash("Succesfully added product.", 'success')
            return redirect(url_for('add_product', ASIN=form.ASIN.data.strip()))
        else:
            flash('Invalid input. Please try again.', 'danger')
            return render_template('add-product.html', form = form)
        
    elif request.method == "GET":
        return render_template('add-product.html', form = form)
    return render_template('add-product.html')

@app.route('/add-to-cart/<int:id>', methods = ["GET", "POST"])
def add_to_cart(id):
    product = Product.query.get(id)
    if product:
        current_user.add_to_cart(product)
    else: 
        flash("Sold Out!", "danger")
    
    return render_template('cart.html', p=product)

    