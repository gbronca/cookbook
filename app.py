from flask import Flask, render_template, session, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

app.config["ALLOWED_EXTENSIONS"] = ['jpg', 'jpeg', 'png']
# Configures the max filesize to 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config["MAX_IMAGE_FILESIZE"] = 1 * 1024 * 1024

mongo = PyMongo(app)

users = mongo.db.users
recipes = mongo.db.recipes
cuisines = mongo.db.cuisines


def allowed_files(filename):
    
    # Check if filename has an file extension
    if not '.' in filename:
        return False

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


''' Return the user in session. If there is no user in session, return None.'''
def get_user():
    username = None

    if 'username' in session:
        username = users.find_one({'username': session['username']})

    return username


'''Return a tuple of cuisines from the cuisines database'''
def get_cuisine():
    cuisine = cuisines.find_one()

    cuisines_tuple = tuple(cuisine['cuisines'])

    return cuisines_tuple

# def get_recipe():
#     try:
#         recipe = recipes.find_one({'name': 'Pasta'})
#         return recipe
#     except:
#         return None

@app.route('/file/<image>')
def file(image):
    return mongo.send_file(image)


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
        
        if existing_user:
            return render_template('register.html', username=username, error='User already exists!')

        password = generate_password_hash(request.form['password'], method='sha256')

        new_user = users.insert_one({'username': request.form['username'],
                        'password': password,
                        'registration_date': datetime.datetime.isoformat(datetime.datetime.now())}).inserted_id

        # Check if new user is successfuly added to the database and if yes creates user session
        if new_user:
            new_user = users.find_one({'_id': ObjectId(new_user)})
            session['username'] = new_user['username']
            session['user_id'] = str(new_user['_id'])

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
    cuisines = get_cuisine()

    if not username:
        return redirect(url_for('login'))

    if request.method == 'POST':
        textarea_ingredients = request.form['ingredients']
        ingredients = textarea_ingredients.split('\n')
        textarea_instructions = request.form['instructions']
        instructions = textarea_instructions.split('\n')

# Test if a file was submitted and it is an image file
# via allowed_imaged function
        if request.files:
            image = request.files['image']
            if image.filename != '' and allowed_files(image.filename):
                image_filename = secure_filename(image.filename)
        else:
            image_filename = ''

        new_recipe_id = recipes.insert_one({
            'user_id': ObjectId(session['user_id']),
            'name': request.form['name'],
            'description': request.form['description'],
            'cooking_time': request.form['cooking-time'],
            'preparation_time': request.form['preparation-time'],
            'servings': request.form['servings'], 
            'ingredients': ingredients,
            'instructions': instructions,
            'image': image_filename,
            'cuisine': request.form['cuisine'],
            'create_date': datetime.datetime.isoformat(datetime.datetime.now())})

# Save image file in the database if image_filename is not empty
# and update the image filename in the recipe document.
# It also ensures an unique filename for each image uploaded by
# adding the recipe's _id and the current date and time to the image's name.
        if image_filename != '':
            image_filename = str(ObjectId(new_recipe_id.inserted_id)) + str(datetime.datetime.isoformat(datetime.datetime.now())) + image_filename
            mongo.save_file(image_filename, image)
            recipes.update_one({'_id': ObjectId(new_recipe_id.inserted_id)}, {'$set': {
                'image': image_filename}})

        return redirect(url_for('index'))

    return render_template('new-recipe.html', username=username, cuisines=cuisines)


@app.route('/recipe/<recipe_id>', methods=['GET', 'POST'])
def recipe(recipe_id):
    username = get_user()
    cuisines = get_cuisine()
    recipe = None
    recipe = recipes.find_one({'_id': ObjectId(recipe_id)})
    if recipe:
        recipe['instructions'] = ''.join(recipe['instructions'])
        recipe['ingredients'] = ''.join(recipe['ingredients'])

    if username:
        if str(username['_id']) == str(recipe['user_id']):
            recipe_owner = True
        else:
            recipe_owner = False
    else:
        recipe_owner = False

    if not recipe_owner:
        return redirect(url_for('load_recipes', recipe_id=recipe_id))

    if request.method == 'POST' and recipe_owner:
        textarea_ingredients = request.form['ingredients']
        ingredients = textarea_ingredients.split('\n')
        textarea_instructions = request.form['instructions']
        instructions = textarea_instructions.split('\n')

        recipe = recipes.update_one({'_id': ObjectId(recipe_id)}, {'$set': {
            'name': request.form['name'],
            'description': request.form['description'],
            'cooking_time': request.form['cooking-time'],
            'preparation_time': request.form['preparation-time'],
            'servings': request.form['servings'], 
            'ingredients': ingredients,
            'instructions': instructions,
            'cuisine': request.form['cuisine'],
            'last_update': datetime.datetime.isoformat(datetime.datetime.now())}})

        recipe = recipes.find_one({'_id': ObjectId(recipe_id)})

    return render_template('recipe.html', username=username, recipe=recipe, recipe_owner=recipe_owner, cuisines=cuisines)


@app.route('/recipes/<recipe_id>')
def load_recipes(recipe_id):
    username = get_user()
    recipe = None
    recipe = recipes.find_one({'_id': ObjectId(recipe_id)})

    return render_template('recipes.html', username=username, recipe=recipe)


@app.route('/user')
def user():
    username = get_user()

    user_recipes = recipes.find({'user_id': ObjectId(username['_id'])})

    return render_template('user.html', username=username, user_recipes=user_recipes)



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
    # app.run(host='127.0.0.1', port=5000)
    # app.secret_key = os.getenv('SECRET')
    # app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=False)