from flask import Flask, render_template, session, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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


# User login. Verify hashed password prior to grant access. 
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
                session['user_id'] = str(current_user['_id'])
                return redirect(url_for('index'))
            else:
                error = 'Username or Password is incorrect'
        else:
            error = 'Username or Password is incorrect'
    
    return render_template('login.html', username=username, error=error)


@app.route('/new-recipe', methods=['GET', 'POST'])
def new_recipe():
    username = get_user()

    if not username:
        return redirect(url_for('login'))

    if request.method == 'POST':
        textarea_ingredients = request.form['ingredients']
        ingredients = textarea_ingredients.split('\n')
        textarea_instructions = request.form['instructions']
        instructions = textarea_instructions.split('\n')

        recipes.insert_one({
            'name': request.form['name'],
            'cooking_time': request.form['cooking-time'],
            'user_id': ObjectId(session['user_id']),
            'ingredients': ingredients,
            'instructions': instructions,
            'cousine': request.form['cousine'],
            'date': datetime.datetime.isoformat(datetime.datetime.now())})

        return redirect(url_for('index'))

    return render_template('new-recipe.html', username=username)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
    # app.run(host='127.0.0.1', port=5000)
    # app.secret_key = os.getenv('SECRET')
    # app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=False)