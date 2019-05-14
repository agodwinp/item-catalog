# Import packages
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, make_response, abort, g
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User, Category, Item
from flask_httpauth import HTTPBasicAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random, string, json, requests, httplib2
from flask_login import logout_user
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Instantiate Flask application and database session
app = Flask(__name__)
auth = HTTPBasicAuth()
engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread':False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Load client ID for Google sign-in
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Function used for generate state
def generateState(sess, key):
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    sess[key] = state
    return state

# JSON API Endpoints
@app.route('/catalog/json')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[i.serialize for i in categories])

@app.route('/catalog/<int:category_id>/json')
@app.route('/catalog/<int:category_id>/items/json')
def categoryJSON(category_id):
    category_items = session.query(Item).filter_by(category_id=category_id)
    return jsonify(Items=[i.serialize for i in category_items])

@app.route('/catalog/<int:category_id>/items/<int:item_id>/json')
def itemsJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)

# Application routes
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def landingPage():
    if request.method == 'GET':
        state = generateState(login_session, 'state')
        return render_template("loginPage.html", STATE=state)
    if request.method == 'POST':
        try:
            #print(1)
            # Check the state variable for extra security, state from ajax request should be the same as random string above
            if login_session['state'] != request.args.get('state'):
                response = make_response(json.dumps('Invalid state parameter.'), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
            # If so, then retrieve token sent by client
            token = request.data
            #print(token)
            #print(2.1)
            # Request an access token from the Google API
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)
            #print(2.2)
            url = ('https://oauth2.googleapis.com/tokeninfo?id_token=%s' % token)
            #url = ("https://oauth2.googleapis.com/token?id_token=%s" % token)
            h = httplib2.Http()
            result = json.loads(h.request(url, 'GET')[1])
            #print(2.3)
            # If there was an error in the access token info, abort
            #print(3)
            if result.get('error') is not None:
                response = make_response(json.dumps(result.get('error')), 500)
                response.headers['Content-Type'] = 'application/json'
                return response
            #print(4)
            # Verify that the access token is used for the intended user
            user_google_id = idinfo['sub']
            if result['sub'] != user_google_id:
                response = make_response(json.dumps("Token's user ID does not match given user ID."), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
            #print(5)
            # Verify that the access token is valid for this app
            if result['aud'] != CLIENT_ID:
                response = make_response(json.dumps("Token's client ID does not match apps."), 401)
                print("Token's client ID does not match apps.")
                response.headers['Content-Type'] = 'application/json'
                return response
            #print(6)
            # Check if the user is already logged in
            stored_access_token = login_session.get('access_token')
            stored_user_google_id = login_session.get('user_google_id')
            if stored_access_token is not None and user_google_id == stored_user_google_id:
                response = make_response(json.dumps("Current user is already connected."), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
            #print(7)
            # Store the access token in the session cookie for later use
            login_session['access_token'] = idinfo
            login_session['user_google_id'] = user_google_id
            # Get user info
            login_session['username'] = idinfo['name']
            login_session['picture'] = idinfo['picture']
            login_session['email'] = idinfo['email']
            # Check if this user exists in database
            #print(8)
            try:
                session.query(User).filter_by(email=login_session['email']).one()
            except:
                newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
                session.add(newUser)
                session.commit()
            #print(9)
            return "Successful"
        except ValueError:
            # Invalid token
            return "ValueError... See trace."
            #pass

@app.route('/logout', methods=['POST'])
def logout():
    #state = generateState(login_session, 'state')
    login_session.clear()
    #return render_template("loginPage.html", STATE=state)
    #return redirect(url_for('showCatalog'))
    return "Logged out"

@app.route('/welcome')
def welcome():
    name = login_session['username']
    picture = login_session['picture']
    return render_template('welcome.html', name=name, picture=picture)

@app.route('/catalog')
def showCatalog(): # READ
    state = generateState(login_session, 'state')
    categories = session.query(Category).all()
    return render_template('allCategories.html', categories=categories, STATE=state)

# PROTECTED
@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory(): # CREATE
    state = generateState(login_session, 'state')
    if request.method == 'GET':
        try:
            user = login_session['username']
            return render_template('newCategory.html', STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showCatalog'))
    else:
        user = session.query(User).filter_by(email=login_session['email']).one()
        user_id = user.id
        newCategory = Category(name=request.form['name'], user_id=user_id)
        session.add(newCategory)
        session.commit()
        flash("New category added!")
        return redirect(url_for('showCatalog'))

# PROTECTED
@app.route('/catalog/<int:category_id>/edit', methods=['GET', 'POST'])
def editCategory(category_id): # UPDATE
    state = generateState(login_session, 'state')
    if request.method == 'GET':
        # Check if they are logged in
        try:
            user = login_session['username']
            # Check if they are authorised to EDIT the category
            category = session.query(Category).filter_by(id=category_id).one()
            category_owner = category.user_id
            user = session.query(User).filter_by(email=login_session['email']).one()
            user_id = user.id
            if category_owner != user_id:
                flash("You are not authorised to edit this category...")
                return redirect(url_for('showCatalog'))
            # If they are, redirect to this
            category_name = category.name
            return render_template('editCategory.html', category_id=category_id, category_name=category_name, STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showCatalog'))
    else:
        editedCategory = session.query(Category).filter_by(id=category_id).one()
        if request.form['name']:
            editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        flash("Category successfully edited!")
        return redirect(url_for('showCatalog'))

# PROTECTED
@app.route('/catalog/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id): # DELETE
    state = generateState(login_session, 'state')
    if request.method == 'GET':
        try:
            user = login_session['username']
            # Check if they are authorised to DELETE the category
            category = session.query(Category).filter_by(id=category_id).one()
            category_owner = category.user_id
            user = session.query(User).filter_by(email=login_session['email']).one()
            user_id = user.id
            if category_owner != user_id:
                flash("You are not authorised to delete this category...")
                return redirect(url_for('showCatalog'))
            # If they are, redirect to this
            category_name = category.name
            return render_template('deleteCategory.html', category_id=category_id, category_name=category_name, STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showCatalog'))
    else:
        deletedCategory = session.query(Category).filter_by(id=category_id).one()
        session.delete(deletedCategory)
        session.commit()
        flash("Category successfully deleted!")
        return redirect(url_for('showCatalog'))

# PROTECTED
@app.route('/catalog/<int:category_id>')
@app.route('/catalog/<int:category_id>/items')
def showItems(category_id): # READ
    state = generateState(login_session, 'state')
    # have an accordian here to expand details
    items = session.query(Item).filter_by(category_id=category_id).all()
    category = session.query(Category).filter_by(id=category_id).one()
    category_name = category.name
    return render_template('showItems.html', items=items, category_id=category_id, category_name=category_name, STATE=state)

# PROTECTED
@app.route('/catalog/<int:category_id>/items/new', methods=['GET', 'POST'])
def newItem(category_id): # CREATE
    state = generateState(login_session, 'state')
    if request.method == 'GET':
        try:
            user = login_session['username']
            return render_template('newItem.html', category_id=category_id, STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showItems', category_id=category_id))
    else:
        user = session.query(User).filter_by(email=login_session['email']).one()
        user_id = user.id
        category = session.query(Category).filter_by(id=category_id).one()
        # Double check that user is authorised to make an item in this category
        if category.user_id != user_id:
            flash("You are not authorised to create an item in this category...")
            return redirect(url_for('showItems', category_id=category_id))
        newItem = Item(title=request.form['title'], description=request.form['description'], category_id=category_id, user_id=user_id)
        session.add(newItem)
        session.commit()
        flash("Item successfully created!")
        return redirect(url_for('showItems', category_id=category_id))

# PROTECTED
@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id): # UPDATE
    state = generateState(login_session, 'state')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'GET':
        try:
            user = login_session['username']
            categories = session.query(Category).all()
            item_name=editedItem.title
            category = session.query(Category).filter_by(id=category_id).one()
            category_name = category.name
            return render_template('editItem.html', categories=categories, category_name=category_name, category_id=category_id, item_id=item_id, item_name=item_name, STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showItems', category_id=category_id))
    else:
        user = session.query(User).filter_by(email=login_session['email']).one()
        user_id = user.id
        # Double check that user is authorised to make an item in this category
        if editedItem.user_id != user_id:
            flash("You are not authorised to edit this item...")
            return redirect(url_for('showItems', category_id=category_id))
        # Update values
        editedItem.title = request.form['title']
        editedItem.description = request.form['description']
        category_id = request.form['category_id']
        editedItem.category_id = category_id
        session.add(editedItem)
        session.commit()
        flash("Item successfully edited!")
        return redirect(url_for('showItems', category_id=category_id))

# PROTECTED
@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id): # DELETE
    state = generateState(login_session, 'state')
    deletedItem = session.query(Item).filter_by(id=item_id).one()
    if request.method == 'GET':
        try:
            user = login_session['username']
            item_name = deletedItem.title
            return render_template('deleteItem.html', category_id=category_id, item_id=item_id, item_name=item_name, STATE=state)
        except KeyError:
            flash("Please log in!")
            return redirect(url_for('showItems', category_id=category_id))
    else:
        user = session.query(User).filter_by(email=login_session['email']).one()
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
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
