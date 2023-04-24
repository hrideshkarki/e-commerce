from flask import Blueprint, flash, redirect, render_template, request, url_for
from .models import Product, User
from flask_login import current_user,login_user, logout_user, login_required
from app import app
from werkzeug.security import generate_password_hash
from .forms import AddProduct, CheckoutForm, EditProfile, EditProduct
import os
import requests as r
from flask import jsonify
from sqlalchemy import desc

PRODUCT_API_KEY = os.environ.get('PRODUCT_API_KEY')

@app.route('/')
def home_page():
    products = Product.query.all()
    return render_template('index.html', products=products)

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
    
@app.route('/products', methods = ["GET", "POST"], defaults={'department': None})
@app.route('/products/<string:department>', methods = ["GET", "POST"])
def products_page(department):
    products_dist = Product.query.distinct(Product.department)
    departments_list = [product.department for product in products_dist]
    
    if department:
        products = Product.query.filter_by(department = department)
    else:
        products = Product.query.all()
    departments_list = [product.department for product in products_dist]
    return render_template('products.html', products=products, departments_list=departments_list)

@app.route('/product/<int:id>')
@login_required
def single_product(id):
    # we need to query to find the product where the ID = the id
    product = Product.query.get(id)
    return render_template('single-product.html', p=product)

@app.route('/add-product/<string:ASIN>', methods = ["GET", "POST"])
@login_required
def add_product(ASIN):
    params = {
        'api_key': 'E0C0A5EFD6384338AE3FE195CC2CA4A7',
        'type': 'product',
        'amazon_domain': 'amazon.com'
    }

    params['asin']= ASIN

    api_result = r.get('https://api.rainforestapi.com/request', params)
    
    data = api_result.json()

    if data["request_info"]["success"] == True:
        flash("Succesfully added product.", 'success')
        product = data["product"]
        
        title = product["title"]
        try:
            price = product["price"]["value"]
        except:
            price = product["buybox_winner"]["price"]["value"]
        image = product["main_image"]["link"]
        department = product["categories"][0]["name"]
        if department == 'All Departments':
            department = product["categories"][1]["name"]
        amazon_link = product["link"]
        try:
            description = product["description"]
        except:
            description = product["feature_bullets"]
        rating = product["rating"]

        new_product = Product(title, price, image, department, amazon_link, description, rating)
        new_product.save_to_db()
                                            # fix this, fix HTML
        return redirect(url_for('admin_add_product'))
    else:
        flash ('Unable to add product.', 'danger')
        return redirect(url_for('admin_add_product'))


@app.route('/remove-item/<int:id>', methods = ["GET", "POST"])
@login_required
def remove_item(id):
    if current_user.is_admin:
        product = Product.query.get(id)
        product.delete_from_db()
    return redirect(url_for('products_page'))

@app.route('/edit-product/<int:id>', methods = ["GET", "POST"])
@login_required
def edit_product(id):
    # we need to query to find the product where the ID = the id
    product = Product.query.get(id)

    form = EditProduct()
    if request.method == "POST":

        # title = form.title.data
        # description = form.description.data
        # price = form.price.data
        # department = form.department.data

        # print(title, description, price,)
        if form.validate():
            title = form.title.data
            description = form.description.data
            price = form.price.data
            department = form.department.data
            product.title = title
            product.description = description
            product.price = price
            product.department = department
            product.save_changes()

            flash("Succesfully updated product.", 'success')
            return redirect(url_for('single_product', id=id))
        else:
            flash('Invalid input. Please try again.', 'danger')
            return render_template('edit-product.html', form = form, p=product)
        
    elif request.method == "GET":
        return render_template('edit-product.html', form = form, p=product)

    return render_template('edit-product.html', form = form, p=product)


@app.route('/add-product', methods = ["GET", "POST"])
@login_required
def admin_add_product():
    if current_user.is_admin:
        form = AddProduct()
        if request.method == "POST":
            if form.validate():
                return redirect(url_for('add_product', ASIN=form.ASIN.data.strip()))
            else:
                flash('Invalid input. Please try again.', 'danger')
                return render_template('add-product.html', form = form)
            
        elif request.method == "GET":
            return render_template('add-product.html', form = form)
        return render_template('add-product.html')
    else:
        # if not admin, just redirect, don't even tell them
        return redirect(url_for('products_page'))


@app.route('/add-to-cart/<int:id>', methods = ["GET", "POST"])
@login_required
def add_to_cart(id):
    product = Product.query.get(id)
    
    # if we end up wanting to have a quantity button
    #times_in_cart = len([p for p in current_user.products if p.id == product.id])
    if product:
        current_user.add_to_cart(product)
    else: 
        flash("Sold Out!", "danger")
    return redirect(url_for('single_product', id=id))

@app.route('/remove-from-cart/<int:id>', methods = ["GET", "POST"])
@login_required
def remove_from_cart(id):
    product = Product.query.get(id)

    if product in current_user.products:
        current_user.remove_from_cart(product)
    elif product: 
        flash('You cannot remove an item from your cart if it is not in your cart', 'danger')
    else:
        flash('That item was not found', 'danger')
    
    #return render_template('single-product.html', p=product)
    # return redirect(url_for('cart', id=id))
    if request.referrer.endswith('/cart'):
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('single_product', id=id))

@app.route('/cart')
def cart():
    cart = current_user.products
    total = 0.0
    for item in cart:
        total += item.price
    return render_template('cart.html', cart=cart, total=("%.2f" % total))
   
@app.route('/empty-cart')
def empty_cart():
    current_user.empty_cart()
    return render_template('cart.html', cart=current_user.products, total=0)

@app.route('/checkout')
def checkout():
    form = CheckoutForm()
    return render_template('checkout.html', form=form)

@app.route('/congrats')
def congrats():
    name = current_user.first_name
    return render_template('congrats.html', name=name)
   