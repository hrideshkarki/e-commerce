from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, InputRequired

class EditProfile(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class AddProduct(FlaskForm):
    ASIN = StringField('ASIN', validators=[DataRequired()])
    submit = SubmitField()

class EditProduct(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = DecimalField('Price', places=2, validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    submit = SubmitField('Submit Changes')