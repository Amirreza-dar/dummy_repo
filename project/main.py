from flask import Blueprint, render_template
from flask_login import login_required, current_user
# from . import db
from flask import Flask, request, session, jsonify
from .database import db
from .objects import questions_object
from flask import flash
from .auth import save_user_session
from.logic import generate_csv
from .ReadData import preprocess_data 


main = Blueprint('main', __name__)

@main.route('/')
def index():
    print('here')
    return render_template('index.html')


@main.route('/prepare')
@login_required 
# TODO: make it login required by adding login property
def prepare():
    # return render_template('prepare.html', name=current_user.name)
    return render_template('prepare.html')

@main.route('/review')
@login_required 
# TODO: make it login required by adding login property
def review():
    # return render_template('prepare.html', name=current_user.name)
    generate_csv()
    path_to_data = session['email'] + '/simulated_new.csv'
    jumps = preprocess_data(path_to_data)
    categories = [[['Left', 'Right']]* len(jumps)][0] # 10-12 pairs
    data = [j['pressure'] for j in jumps]
    sizes = [j['jump duration']*200 for j in jumps]
    print('#####################################')
    print(sizes)
    # data = [[30, 70], [50, 50], [30, 70], [50, 50], [30, 70], [50, 50], [30, 70], [50, 50], [30, 70], [50, 50]] # Corresponding values for the categories
    # sizes = [100, 120, 100, 120,100, 120,100, 120,100, 120] # Sizes for each pie chart
    colors = [['#006400', '#008000'] ,['#006400', '#008000'],['#006400', '#008000'],['#CCCC00', '#FFFF00'],['#006400', '#008000'],['#8B0000', '#FF0000'],['#006400', '#008000'],['#006400', '#008000']]
                #   ['#CCCC00', '#FFFF00'], ['#8B0000', '#FF0000'] 
    return render_template('review.html', categories=categories, data=data, sizes=sizes, colors=colors)

    # return render_template('review.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# @main.route('/admin')
# @login_required
# def admin():
#     if not current_user.is_admin:
#         flash('Unauthorized access.')
#         return render_template('admin.html') # Redirect non-admins to the main page

#     # Admin dashboard logic goes here
#     return render_template('admin_dashboard.html')

# prapare page logic:

@main.route('/save-user-choices', methods=['POST'])
def save_user_choices():
    # Extract choices from request.form and save them
    session['feeling'] = request.form.get('feeling')
    # Save the data as needed
    print(session['feeling'])
    return '', 204  # No content to return

@main.route('/save-game-selection', methods=['POST'])
def save_game_selection():
    # Extract game choice and save it
    session['game'] = request.form.get('gameLevel')
    # Save the data as needed
    print(session['game'])
    
    return '', 204  # No content to return


# review page logic:

@main.route('/save-answer', methods=['POST'])
def save_answer():
    data = request.get_json()
    question_id = data.get('questionId')
    answer = data.get('answer')
    session[question_id] = answer
    # Process the answer, e.g., save to database
    print(question_id, session[question_id])
    return jsonify({'status': 'success'})


# display user choices 

@main.route('/get_session_data')
def get_session_data():
    # Assuming session data is stored as a dictionary
    # readiness = session.get('readiness', 'Default readiness info')
    # accuracy = session.get('accuracy', 'Default accuracy info')
    # challenge = session.get('challenge', 'Default challenge info')
    # impact = session.get('impact', 'Default impact info')
    readiness = session.get('feeling', 'Default readiness info')
    accuracy = session.get('main', 'Default accuracy info')
    challenge = session.get('q2', 'Default challenge info')
    impact = session.get('q3', 'Default impact info')

    # before returning user data, add record to the database
    save_user_session(current_user.id, session)

    return jsonify({
        'readiness': readiness,
        'accuracy': accuracy,
        'challenge': challenge,
        'impact': impact
    })

# @app.route('/')
# def pie_charts():
    # Example data
    # categories = [['Category 1', 'Category 2'], ['Category 3', 'Category 4'], ...] # 10-12 pairs
    # data = [[30, 70], [50, 50], ...] # Corresponding values for the categories
    # sizes = [100, 120, ...] # Sizes for each pie chart
    # colors = [['#ff6384', '#36a2eb'], ['#cc65fe', '#ffce56'], ...] # Color pairs for each chart
    
    # return render_template('pie_charts.html', categories=categories, data=data, sizes=sizes, colors=colors)


### Run the function to add an admin user

# from .models import User
# from .database import db
# from werkzeug.security import generate_password_hash

# @main.route('/add_admin')
# def add_admin_user():
#     # Admin user credentials
#     admin_email = "admin@example.com"
#     admin_password = "admin"  # You should choose a strong password

#     # Check if admin user already exists
#     existing_admin = User.query.filter_by(email=admin_email).first()
#     if existing_admin:
#         print("An admin user with this email already exists.")
#         return

#     # Create an admin user instance
#     admin_user = User(
#         email=admin_email,
#         password=generate_password_hash(admin_password, method='pbkdf2'),
#         is_admin=True
#     )

#     # Add the admin user to the session and commit
#     db.session.add(admin_user)
#     db.session.commit()
#     print("Admin user added successfully.")
#     return "Admin added"





# @main.route('/selectgame')
# def selectgame():
#     return render_template('selectgame.html')


# @main.route('/difficulty', methods=['POST'])
# def difficulty():
#     session['game'] = request.form.get('game')
#     # print(request.form)
#     # print(f'the name of the game is {session.get}')
#     return render_template('difficulty.html', game=session.get('game'))

# @main.route('/gamecheck', methods=['GET','POST'])
# def gamecheck():
#     session['difficulty'] = request.form.get('difficulty')
#     print(request.form.get('game'))
#     return render_template('gamecheck.html', game = session.get('game'), difficulty = session.get('difficulty'))

# @main.route('/index2')
# def index2():
#     return render_template('index2.html')


# @main.route('/questions' , methods=['GET', 'POST'])
# def questions():
#     if request.method == 'POST':
#         if questions_object.id == 4:
#             questions_object.id = 0
#             return render_template('/')

#         questions_object.id += 1
#         return render_template('questions.html', question=questions_object)
    
#     return render_template('questions.html', question=questions_object) 

# @main.route('/results')
# def results():
#     return render_template('results.html')

# @main.route('/gamedemo')
# def gamedemo():
#     return render_template('gamedemo.html')

# @main.route('/menu')
# def menu():
#     return render_template('menu.html')
