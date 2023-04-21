from flask import Blueprint, flash, redirect, render_template, request, url_for
from .models import User
from flask_login import current_user,login_user, logout_user, login_required
from app import app

@app.route('/')
def homePage():
    return render_template('home.html')