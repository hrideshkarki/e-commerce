from . import api
from ..models import User
from flask import request
from werkzeug.security import check_password_hash
from ..apiauthhelper import basic_auth

@api.post('/signup')
def signUpAPI():
    data = request.json

    username = data['username']
    email = data['email']
    password = data['password']

    user = User.query.filter_by(username = username).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'Please choose a different username.'
        }, 400
    user = User.query.filter_by(email = email).first()
    if user:
        return {
            'status': 'not ok',
            'message': 'That email is already in use.'
        }, 400

    user = User(username, email, password)
    user.saveToDB()
    return {
        'status': 'ok',
        'message': "You have successfully created an account."
    }, 201


@api.post('/login')
@basic_auth.login_required
def loginAPI():
    return {
        'status': 'ok',
        'message': "You have successfully logged in.",
        'data': basic_auth.current_user().to_dict()
    }, 200






# from . import api
# from ..models import User
# from flask import request
# from werkzeug.security import check_password_hash
# from ..apiauthhelper import basic_auth, basic_auth_required

# @api.post('/signup')
# def signUpAPI():
#     data = request.json

#     print(data)

#     first_name = data['first_name']
#     last_name = data['last_name']
#     username = data['username']
#     email = data['email']
#     password = data['password']

#     user = User.query.filter_by(username = username).first()
#     if user:
#         return {
#             'status': 'not ok',
#             'message': 'Please choose a different username.'
#         }, 400
    
#     user = User.query.filter_by(email = email).first()
#     if user:
#         return {
#             'status': 'not ok',
#             'message': 'That email is already in use.'
#         }, 400

#     user = User(first_name, last_name, username, email, password)
#     user.save_to_db()
#     return {
#         'status': 'ok',
#         'message': "You have successfully created an account."
#     }, 201


# @api.post('/login')
# @basic_auth_required
# def loginAPI(user):
#     return {
#         'status': 'ok',
#         'message': "You have successfully logged in.",
#         'data': user.to_dict()
#     }, 200

