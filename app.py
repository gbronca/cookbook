from flask import Flask, render_template, session, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

mongo = PyMongo(app)

users = mongo.db.users
recipes = mongo.db.recipes

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


def insert_recipe():
    try:
        recipes.insert_one({'name': 'Pasta',
                            'cooking_time': 30,
                            'preparation_time': 25,
                            'nutrition': {
                                'calories': 200,
                                'carb_content': 20,
                                'sugar_content': 15,
                                'fat_content': 40
                            },
                            'category': 'Pasta',
                            'cousine': 'Italian',
                            'ingredients': ['Pasta', 'Tomato Sauce', 'Salt'],
                            'instructions': ['Boil water', 'add salt', 'insert pasta', 'cook for 10 min'],
                            'registration_Date' : datetime.datetime.isoformat(datetime.datetime.now())})
        return True
    except:
        return False


@app.route('/')
def index():
    user = get_user()

    recipes_list = recipes.find()
    return render_template('index.html', recipes=recipes_list)


''' Register a user on the database '''
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


if __name__ == '__main__':
    app.run()
    # app.run(host='127.0.0.1', port=5000)
    # app.secret_key = os.getenv('SECRET')
    # app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=False)