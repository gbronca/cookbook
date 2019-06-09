# import os, json
from flask import Flask, render_template, session, redirect, request, url_for
from flask_pymongo import PyMongo
import datetime

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

mongo = PyMongo(app)

users = mongo.db.users
recipes = mongo.db.recipes


def insert_user():
    try:
        users.insert_one({'email' : 'Giovanni', 
                        'username' : 'Couto',
                        'password' : 'password',
                        'registration_Date' : datetime.datetime.isoformat(datetime.datetime.now())})
        return True
    except:
        return False


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


def retrieve_user():
    try:
        user = users.find_one({'username': 'Couto'})
        return user
    except:
        return None


def retrieve_recipe():
    try:
        recipe = recipes.find_one({'name': 'Pasta'})
        return recipe
    except:
        return None


@app.route('/')
def index():
    recipes_list = recipes.find()
    return render_template('index.html', recipes=recipes_list)



if __name__ == '__main__':
    app.run()
    # app.run(host='127.0.0.1', port=5000)
    # app.secret_key = os.getenv('SECRET')
    # app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=False)