from flask import Blueprint, flash, redirect, render_template, request, url_for
from .models import User
from flask_login import current_user,login_user, logout_user, login_required
from app import app
from werkzeug.security import generate_password_hash
from .forms import  EditProfile

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