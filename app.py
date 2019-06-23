from flask import Flask, render_template, session, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

mongo = PyMongo(app)

users = mongo.db.users
recipes = mongo.db.recipes


''' Return the user in session. If there is no user in session, return None.'''
def get_user():
    username = None

    if 'username' in session:
        username = users.find_one({'username': session['username']})

    return username


def get_recipe():
    try:
        recipe = recipes.find_one({'name': 'Pasta'})
        return recipe
    except:
        return None


@app.route('/')
def index():
    username = get_user()

    recipes_list = recipes.find()
    return render_template('index.html', recipes=recipes_list, username=username)


# Register a new user.
# Before adding the user to the database it checks first if there is no user with the same name
@app.route('/register', methods=['GET', 'POST'])
def register():
    username = get_user()

    if request.method == 'POST':

        existing_user = users.find_one({'username': request.form['username']})
        print(request.form['username'])
        print(existing_user)
        
        if existing_user:
            return render_template('register.html', username=username, error='User already exists!')

        password = generate_password_hash(request.form['password'], method='sha256')
        users.insert_one({'username': request.form['username'],
                        'password': password,
                        'registration_date': datetime.datetime.isoformat(datetime.datetime.now())})

        return redirect(url_for('index'))
    
    return render_template('register.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = get_user()
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        current_user = users.find_one({'username': username})

        if current_user:
            if check_password_hash(current_user['password'], password):
                session['username'] = current_user['username']
                return redirect(url_for('index'))
            else:
                error = 'Username or Password is incorrect'
        else:
            error = 'Username or Password is incorrect'
    
    return render_template('login.html', username=username, error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
    # app.run(host='127.0.0.1', port=5000)
    # app.secret_key = os.getenv('SECRET')
    # app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=False)