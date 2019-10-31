# Cookbook Project

About a year ago I have decided to adopt a healthier lifestyle and part of this change was based on healthy eating. I have seen several interesting recipes online but had no system to store them so I could refer back when needed.

The idea of building a recipes website for my 4th project for the Code Institute Full Stack Developer Course was just inline with a personal project.

The Recipes app can be viewed [here](http://gb-cookbook.herokuapp.com/)

## UX

### User Stories

1. As a visitor, I would like to be able to browse and search for recipes that fit some specific criteria.

2. A user should be able to search for recipes by name.

3. A user should be able to search for recipes by popularity (likes).

4. A user should be able to search for recipes by cuisine.

5. A user should be able to open a recipe and see ingredients, instructions and cooking time.

6. A user can create an account.

7. A registered user:
    * Can like recipes;
    * Flag recipes as cooked, meaning they have tried it;
    * Can add new recipes to the site;
    * Can edit their recipes;
    * Can delete their recipe.

### Features

* User registration: although it is a simple user registration, the password is encrypted using generate_password_hash function from Werkzeug Security module.

* User login: Allows a user to log in on the app. Once a user is logged in, it allows a user to like recipes, mark them as cooked, add new recipes and even edit/delete the ones created by the user.

* Search tab: Allow users to search a recipe by cuisine, likes/most recent/name and/or keyword.

* A Search box in the navigation menu: Lists all recipes with the searched keyword.

* User page: List all recipes uploaded by the user, with the option to edit or delete the recipe.

* Recipe page: presents information and instructions about a specific recipe. If the recipe belongs to the user, the system allows the user to edit the recipe.

#### features to add

* Ability to like a recipe from the main page, if the user is logged in.

* Ability to comment on recipes and like other users' comments.

* Pagination

* Add cuisines

* Export to PDF

* Save all images in AWS instead of MongoDB.

* If there is a server error, an error page should show with an error message and redirect the user to the main page after a couple of seconds.

### Wireframes

![Home page Desktop version](docs/wireframes/home-page.png)

![New Recipe Desktop version](docs/wireframes/add-recipe-page.png)

![User Account Desktop version](docs/wireframes/user-account-page.png)

## Database Schema

The basic database diagram is as follow:

![Database Diagram](docs/database/cookbook-database-diagram.png)

More information can be read in [Cookbook Documentation](docs/database/Cookbook-documentation.pdf)

## Technologies

* HTML 5

* CSS 3

* [Bootstrap](https://getbootstrap.com/)

* Javascript

* [Python 3](https://www.python.org/)

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)

* [MongoDB](https://www.mongodb.com/)

## Tests

All pages have been tested extensively during development by myself. Once deployed, the app was tested by a small number of people, mainly family members and work colleagues that have reported any issues they have found.

I've personally tested the site on Firefox, Safari and Chrome for macOS and the same browsers for in Windows 10.

The site was tested for responsiveness using devtools and also running the app on the iPhone.

* HTML validated by [The W3C Markup Validation Service](https://validator.w3.org/)

* CSS validated by [The W3C CSS Validation Service - Jigsaw](https://jigsaw.w3.org/css-validator/)

* Python compliant to PEP8 via [Pylint](https://pylint.org/).

### Compatibility

Tested on:

* Google Chrome

* Firefox

* Safari

## Deployment

The project is hosted on Heroku. For it to run correctly the following is required:

* A Procfile that instructs Heroku how to run the app.

* requirements.txt. This file informs Heroku what dependencies are required to run the app correctly. It is created by typing on the terminal `pip freeze > requirements.txt`.

* Create a new app in Heroku

* Setup in Heroku the environment variables required to successfully run the app in Settings, Config Vars.

```python
MONGO_DBNAME
MONGO_URI
SECRET_KEY
PORT
IP
```

* Connect Heroku to the project's repository on Github and setup automatic deployment. Heroku then will build a new version of the app every time a new deployment is pushed to Github.

### Local Deployment

* Clone the repository

* Create a virtual environment and install the dependencies.

* setup the environment variables

```python
app.config['MONGO_DBNAME'] = os.getenv("MONGO_DBNAME")
app.config['MONGO_URI'] = os.getenv("MONGO_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
```

* On terminal type `python3 app.py` to run the app.
