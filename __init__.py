# !/usr/bin/env python3
# Import packages
import os
import random
import string
import json
import httplib2
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from werkzeug.utils import secure_filename
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import flash, make_response
from flask import session as login_session
from database import Base, User, Category, Item
from flask_httpauth import HTTPBasicAuth

UPLOAD_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Instantiate Flask application and database session
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'AUnm0\-7Hu$cmOPp+x^j]!34an*js.(8j'
auth = HTTPBasicAuth()
engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Load client ID for Google sign-in
CLIENT_ID = "169649741771-41dfhe2bc1kmjkfq1r97ir1b24cr9lqm.apps.googleusercontent.com"


# Function used for generate state
def generateState(sess, key):
    """
    Generate state used for application cookie.

    Creates a randon string of numbers and letters to encrypt the
    users session for use within a cookie.
    """
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.digits) for x in xrange(32))
    sess[key] = state
    return state


def allowed_file(filename):
    """
    Checks if uploaded file is allowed.

    File type checker used when user uploads an image for a
    new category.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Function for serializing items in category
def serialize_category(category):
    """
    Create JSON formatted string for category and items.

    Serialize a category with all its items ready for consumption
    within the catalog API endpoint.
    """
    items = session.query(Item).filter_by(category_id=category.id)
    return {
        'id': category.id,
        'name': category.name,
        'items': [i.serialize for i in items]
    }


# JSON API Endpoints
@app.route('/catalog/json')
def catalogJSON():
    """
    Catalog API endpoint.

    Returns JSON formatted catalog data with all categories and items.
    """
    categories = session.query(Category).all()
    return jsonify(Categories=[serialize_category(i) for i in categories])


@app.route('/catalog/<int:category_id>/json')
@app.route('/catalog/<int:category_id>/items/json')
def categoryJSON(category_id):
    """
    Category API endpoint.

    Returns JSON formatted category data with all items within it,
    based on category_id.
    """
    category_items = session.query(Item).filter_by(category_id=category_id)
    return jsonify(Items=[i.serialize for i in category_items])


@app.route('/catalog/<int:category_id>/items/<int:item_id>/json')
def itemsJSON(category_id, item_id):
    """
    Item API endpoint.

    Returns JSON formatted item data, based on category_id and
    user_id.
    """
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)


# Application routes
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def landingPage():
    """
    Landing page of web application.

    This web page provides the landing page for the root URL. The
    user can enter the site, or Login via Google Sign-In.
    """
    if request.method == 'GET':
        state = generateState(login_session, 'state')
        return render_template("loginPage.html", STATE=state)
    if request.method == 'POST':
        try:
            # Check the state variable for extra security
            # state from ajax request should be the same as
            # random string above
            if login_session['state'] != request.args.get('state'):
                message = "Invalid state parameter."
                response = make_response(json.dumps(message), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
            # If so, then retrieve token sent by client
            token = request.data
            # Request an access token from the Google API
            idinfo = id_token.verify_oauth2_token(token,
                                                  google_requests.Request(),
                                                  CLIENT_ID)
            token_url = "https://oauth2.googleapis.com/tokeninfo?id_token={}"
            url = (token_url.format(token))
            h = httplib2.Http()
            result = json.loads(h.request(url, 'GET')[1])
            # If there was an error in the access token info, abort
            if result.get('error') is not None:
                response = make_response(json.dumps(result.get('error')), 500)
                response.headers['Content-Type'] = 'application/json'
                return response
            # Verify that the access token is used for the intended user
            user_google_id = idinfo['sub']
            if result['sub'] != user_google_id:
                message = "Token's user ID does not match given user ID."
                response = make_response(json.dumps(message), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
            # Verify that the access token is valid for this app
            if result['aud'] != CLIENT_ID:
                message = "Token's client ID does not match apps."
                response = make_response(json.dumps(message), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
            # Check if the user is already logged in
            stored_access_token = login_session.get('access_token')
            stored_user_google_id = login_session.get('user_google_id')
            if stored_access_token is not None:
                if user_google_id == stored_user_google_id:
                    message = "Current user is already connected."
                    response = make_response(json.dumps(message), 200)
                    response.headers['Content-Type'] = 'application/json'
                    return response
                message = "User authentication error."
                response = make_response(json.dumps(message), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
            # Store the access token in the session cookie for later use
            login_session['access_token'] = idinfo
            login_session['user_google_id'] = user_google_id
            # Get user info
            login_session['username'] = idinfo['name']
            login_session['picture'] = idinfo['picture']
            login_session['email'] = idinfo['email']
            # Check if this user exists in database
            try:
                email = login_session['email']
                user = session.query(User).filter_by(email=email).one()
            except KeyError:
                newUser = User(name=login_session['username'],
                               email=login_session['email'],
                               picture=login_session['picture'])
                session.add(newUser)
                session.commit()
            return "Successful"
        except ValueError:
            # Invalid token
            return "ValueError... See trace."


@app.route('/logout', methods=['POST'])
def logout():
    """
    Logs the user out.

    This simple route logs the user out of the application and clears
    the session cookie.
    """
    login_session.clear()
    return "Logged out"


@app.route('/welcome')
def welcome():
    """
    Welcome page after logging in.

    After the user logs in, they will be redirected to this login
    page where they'll be welcomed by their name and Google profile
    image.
    """
    name = login_session['username']
    picture = login_session['picture']
    return render_template('welcome.html', name=name, picture=picture)


@app.route('/catalog')
def showCatalog():
    """
    Displays all categories within the catalog.

    This page will display all categories within the catalog to the
    user. If logged in, they will have the ability to add a new
    category.
    """
    state = generateState(login_session, 'state')
    categories = session.query(Category).all()
    return render_template('allCategories.html', categories=categories,
                           STATE=state, session=login_session)


@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory():
    """
    Add a new category within the catalog.

    This page will provide a form for the user to create a new catalog
    category. This page is only accessible once logged in, and the
    created category will be owned by the logged in user.
    """
    state = generateState(login_session, 'state')
    if request.method == 'GET':
        try:
            user = login_session['username']
            return render_template('newCategory.html', STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showCatalog'))
    else:
        email = login_session['email']
        user = session.query(User).filter_by(email=email).one()
        user_id = user.id
        name = request.form['name']
        image = request.files['image']
        # check if the post request has the file part
        if not image:
            if name:
                newCategory = Category(name=name, user_id=user_id)
                session.add(newCategory)
                session.commit()
                flash("New category added!")
                return redirect(url_for('showCatalog'))
            flash("Please choose a name!")
            return redirect(url_for('newCategory'))
        file = request.files['image']
        if file and allowed_file(file.filename):
            if name:
                filename = secure_filename(file.filename)
                file.save(app.config['UPLOAD_FOLDER'] + filename)
                newCategory = Category(name=name, image=filename,
                                       user_id=user_id)
                session.add(newCategory)
                session.commit()
                flash("New category added!")
                return redirect(url_for('showCatalog'))
            flash("Please choose a name!")
            return redirect(url_for('newCategory'))


@app.route('/catalog/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id):
    """
    Edit a category within the catalog.

    This page will provide a form for the user to edit an existing catalog
    category. This page is only accessible once logged in, and the user
    can only access this page if they created the category.
    """
    state = generateState(login_session, 'state')
    if request.method == 'GET':
        # Check if they are logged in
        try:
            user = login_session['username']
            # Check if they are authorised to EDIT the category
            category = session.query(Category).filter_by(id=category_id).one()
            category_owner = category.user_id
            user = session.query(User).filter_by(email=login_session['email'])
            user = user.one()
            user_id = user.id
            if category_owner != user_id:
                flash("You are not authorised to edit this category...")
                return redirect(url_for('showCatalog'))
            # If they are, redirect to this
            category_name = category.name
            return render_template('editCategory.html',
                                   category_id=category_id,
                                   category_name=category_name, STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showCatalog'))
    else:
        editedCategory = session.query(Category).filter_by(id=category_id)
        editedCategory = editedCategory.one()
        name = request.form['name']
        if name:
            editedCategory.name = request.form['name']
            session.add(editedCategory)
            session.commit()
            flash("Category successfully edited!")
            return redirect(url_for('showCatalog'))
        flash("Please choose a name!")
        return redirect(url_for('editCategory', category_id=category_id))


@app.route('/catalog/<int:category_id>/delete', methods=['GET', 'POST'])
def deleteCategory(category_id):
    """
    Delete a category within the catalog.

    This page will provide a form for the user to complete that
    will delete an existing catalog category. This page is only accessible
    once logged in, and the user can only access this page if they created
    the category.
    """
    state = generateState(login_session, 'state')
    if request.method == 'GET':
        try:
            user = login_session['username']
            # Check if they are authorised to DELETE the category
            category = session.query(Category).filter_by(id=category_id).one()
            category_owner = category.user_id
            user = session.query(User).filter_by(email=login_session['email'])
            user = user.one()
            user_id = user.id
            if category_owner != user_id:
                flash("You are not authorised to delete this category...")
                return redirect(url_for('showCatalog'))
            # If they are, redirect to this
            category_name = category.name
            return render_template('deleteCategory.html',
                                   category_id=category_id,
                                   category_name=category_name, STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showCatalog'))
    else:
        deletedCategory = session.query(Category).filter_by(id=category_id)
        deletedCategory = deletedCategory.one()
        session.delete(deletedCategory)
        session.commit()
        flash("Category successfully deleted!")
        if deletedCategory.image:
            image_to_delete = deletedCategory.image
            if os.path.exists(app.config['UPLOAD_FOLDER'] + image_to_delete):
                os.remove(app.config['UPLOAD_FOLDER'] + image_to_delete)
        return redirect(url_for('showCatalog'))


@app.route('/catalog/<int:category_id>')
@app.route('/catalog/<int:category_id>/items')
def showItems(category_id):
    """
    Displays all items within a category.

    This page will display all items within a catalog category. If logged in
    and the user has ownership of the category, they will have the ability
    to add a new item, or edit and delete an item.
    """
    state = generateState(login_session, 'state')
    items = session.query(Item).filter_by(category_id=category_id).all()
    category = session.query(Category).filter_by(id=category_id).one()
    user = session.query(User).filter_by(id=category.user_id).one()
    user_email = user.email
    return render_template('showItems.html', items=items,
                           category_id=category_id, category=category,
                           STATE=state, session=login_session,
                           user_email=user_email)


@app.route('/catalog/<int:category_id>/items/new', methods=['GET', 'POST'])
def newItem(category_id):
    """
    Add a new item within a category.

    This page will provide a form for the user to create a new item within
    a category. This page is only accessible once logged in and if the user
    has ownership of the category that the item is being added to.
    """
    state = generateState(login_session, 'state')
    if request.method == 'GET':
        try:
            user = login_session['username']
            owner = session.query(User).filter_by(email=login_session['email'])
            owner = owner.one()
            user_id = owner.id
            category = session.query(Category).filter_by(id=category_id).one()
            # Double check that user is authorised to make an item
            # in this category
            if category.user_id != user_id:
                flash("Please log in!")
                return redirect(url_for('showItems', category_id=category_id))
            return render_template('newItem.html', category_id=category_id,
                                   STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showItems', category_id=category_id))
    else:
        user = session.query(User).filter_by(email=login_session['email'])
        user = user.one()
        user_id = user.id
        category = session.query(Category).filter_by(id=category_id).one()
        title = request.form['title']
        description = request.form['description']
        # Double check that user is authorised to make an item in this category
        if category.user_id != user_id:
            flash("You are not authorised to create an item in this category.")
            return redirect(url_for('showItems', category_id=category_id))
        if title and description:
            newItem = Item(title=title,
                           description=description,
                           category_id=category_id, user_id=user_id)
            session.add(newItem)
            session.commit()
            flash("Item successfully created!")
            return redirect(url_for('showItems', category_id=category_id))
        flash("Please complete the form!")
        return redirect(url_for('newItem', category_id=category_id))


@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    """
    Edit an item within a category.

    This page will provide a form for the user to edit an existing item
    within a category. This page is only accessible once logged in and
    if the user has ownership of the category that the item is being
    edited within.
    """
    state = generateState(login_session, 'state')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'GET':
        try:
            user = login_session['username']
            categories = session.query(Category).all()
            item_name = editedItem.title
            category = session.query(Category).filter_by(id=category_id).one()
            category_name = category.name
            return render_template('editItem.html', categories=categories,
                                   category_name=category_name,
                                   category_id=category_id, item_id=item_id,
                                   item_name=item_name, STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showItems', category_id=category_id))
    else:
        user = session.query(User).filter_by(email=login_session['email'])
        user = user.one()
        user_id = user.id
        title = request.form['title']
        description = request.form['description']
        cat_id = request.form['category_id']
        # Double check that user is authorised to make an item in this category
        if editedItem.user_id != user_id:
            flash("You are not authorised to edit this item...")
            return redirect(url_for('showItems', category_id=category_id))
        # Update values
        if title and description and cat_id:
            editedItem.title = title
            editedItem.description = description
            category_id = cat_id
            editedItem.category_id = category_id
            session.add(editedItem)
            session.commit()
            flash("Item successfully edited!")
            return redirect(url_for('showItems', category_id=category_id))
        flash('Please complete the form!')
        return redirect(url_for('editItem', category_id=category_id,
                        item_id=item_id))


@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    """
    Delete an item within a category.

    This page will provide a form for the user to delete an existing item
    within a category. This page is only accessible once logged in and if
    the user has ownership of the category that the item is being deleted
    from.
    """
    state = generateState(login_session, 'state')
    deletedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'GET':
        try:
            user = login_session['username']
            item_name = deletedItem.title
            return render_template('deleteItem.html', category_id=category_id,
                                   item_id=item_id, item_name=item_name,
                                   STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showItems', category_id=category_id))
    else:
        user = session.query(User).filter_by(email=login_session['email'])
        user = user.one()
        user_id = user.id
        # Double check that user is authorised to make an item in this category
        if deletedItem.user_id != user_id:
            flash("You are not authorised to delete this item...")
            return redirect(url_for('showItems', category_id=category_id))
        session.delete(deletedItem)
        session.commit()
        flash("Item successfully deleted!")
        return redirect(url_for('showItems', category_id=category_id))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
