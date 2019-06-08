import os, json
from flask import Flask, render_template, session, redirect, request, url_for, g
from flask_pymongo import PyMongo
import bcrypt, datetime

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

mongo = PyMongo(app)

users = mongo.db.users
recipes = mongo.db.recipes


def insert_user():
    users.insert_one({'email' : 'Giovanni', 
                    'username' : 'Couto',
                    'password' : 'password',
                    'registration_Date' : datetime.datetime.isoformat(datetime.datetime.now())})

    return True


def insert_recipe():
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


def retrieve_user():
    user = users.find_one({'username': 'Couto'})
    return user


def retrieve_recipe():
    recipe = recipes.find_one({'name': 'Pasta'})
    return recipe




