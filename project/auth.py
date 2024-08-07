from flask import Blueprint, render_template, redirect, url_for , request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User, UserSession
from .database import db
from flask import jsonify
from datetime import datetime
import json
import os
from flask import session
# Example of a complex object



auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('index.html')

@auth.route('/login', methods=['POST'])
def login_post():

    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    # remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # login code goes here
    # login_user(user, remember=remember)
    # dir = f'report/{str(generate_password_hash(password, method='pbkdf2'))}'
    # os.mkdir(dir)
    # session['user_report_dir'] = dir
    session['email'] = f'report/{email}'
    login_user(user)
    # check if logged_in user is admin then redirect to admin.dashboard
    #TODO write the correct directory here
    if user.is_admin:
        return redirect(url_for('auth.admin'))
    
    return redirect(url_for('main.prepare'))

@auth.route('/signup')
def signup():
    # return render_template('signup.html')
    pass

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        # return redirect(url_for('auth.signup'))
        return jsonify({'message': 'Email address already exists'}), 400
        

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    # return redirect(url_for('auth.login'))
    # return redirect(url_for('main.index'))
    # dir = f'report/{str(generate_password_hash(password, method='pbkdf2'))}'
    # # os.mkdir(dir)
    # session['user_report_dir'] = dir
    return redirect(url_for('main.index', scrollTo='intro'))


@auth.route('/logout')
@login_required
def logout():
    # return render_template('login.html')
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/save_user_session')
@login_required
def save_user_session(user_id, session_data):
    # print(session_data['_id'], session_data['_user_id'], user_id)
    user_session = UserSession(user_id=user_id)
    last_login = datetime.utcnow()
    session_data = {
        'TimeStamp' : last_login.strftime('%Y-%m-%d %H:%M:%S'),
        'Feeling' : session_data['feeling'],
        'Difficulty' : session_data['game'],
        'Question1' : session_data['main'],
        'Question2' : session_data['q2'],
        'Question3' : session_data['q3']
    }
    user_session.set_session_data(session_data)
    db.session.add(user_session)
    db.session.commit()
    print('record added!')

@auth.route('/get_user_sessions')
@login_required
def get_user_sessions(user_id):
    user = User.query.get(user_id)
    if not user:
        return None  # Or handle as appropriate
    return user.sessions


@auth.route('/admin/users')
def admin():
    users = User.query.all()  # Fetch all users
    users_data = []
    for user in users:
        user_sessions = UserSession.query.filter_by(user_id=user.id).all()  # Fetch sessions for each user
        # sessions_data = [session.get_session_data() for session in user_sessions]  # Extract session data
        sessions_data = [json.dumps(session.get_session_data(), indent=4) for session in user_sessions]
        # users_data.append({
        users_data.append({
            'email': user.email,
            'name': user.name,
            'sessions': sessions_data
        })
    return render_template('admin.html', users=users_data)

