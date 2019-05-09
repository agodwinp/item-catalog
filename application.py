from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, make_response, abort, g
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User, Category, Item
from flask_httpauth import HTTPBasicAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random, string, json, requests, httplib2

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

app = Flask(__name__)
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread':False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

def generateState(sess, key):
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    sess[key] = state
    return state


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def landingPage():
    if request.method == 'GET':
        state = generateState(login_session, 'state')
        return render_template("loginPage.html", STATE=state)
    if request.method == 'POST':
        try:
            # Check the state variable for extra security, state from ajax request should be the same as random string above
            if login_session['state'] != request.args.get('state'):
                response = make_response(json.dumps('Invalid state parameter.'), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
            # If so, then retrive token sent by client
            token = request.data
            # Request an access token from the Google API
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)
            url = ('https://oauth2.googleapis.com/tokeninfo?id_token=%s' % token)
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
                response = make_response(json.dumps("Token's user ID does not match given user ID."), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
            # Verify that the access token is valid for this app
            if result['aud'] != CLIENT_ID:
                response = make_response(json.dumps("Token's client ID does not match apps."), 401)
                print("Token's client ID does not match apps.")
                response.headers['Content-Type'] = 'application/json'
                return response
            # Check if the user is already logged in
            stored_access_token = login_session.get('access_token')
            stored_user_google_id = login_session.get('user_google_id')
            if stored_access_token is not None and user_google_id == stored_user_google_id:
                response = make_response(json.dumps("Current user is already connected."), 200)
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
                session.query(User).filter_by(email=login_session['email']).one()
            except:
                newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
                session.add(newUser)
                session.commit()
            return "Successful"
        except ValueError:
            # Invalid token
            pass


@app.route('/catalog')
def showCatalog(): # READ
    state = generateState(login_session, 'state')
    #return login_session['picture']
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
            return render_template("unAuthorisedEntry.html", STATE=state)
    else:
        user = session.query(User).filter_by(email=login_session['email']).one()
        user_id = user.id
        newCategory = Category(name=request.form['name'], user_id=user_id)
        session.add(newCategory)
        session.commit()
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
                return render_template("unAuthorisedEntry.html", STATE=state)
            # If they are, redirect to this
            category_name = category.name
            return render_template('editCategory.html', category_id=category_id, category_name=category_name, STATE=state)
        except KeyError:
            return render_template("unAuthorisedEntry.html")
    else:
        editedCategory = session.query(Category).filter_by(id=category_id).one()
        if request.form['name']:
            editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        return redirect(url_for('showCatalog'))


# PROTECTED
@app.route('/catalog/<int:category_id>/delete', methods=['GET','POST'])
def deleteCategory(category_id): # DELETE
    state = generateState(login_session, 'state')
    if request.method == 'GET':
        try:
            user = login_session['username']
            # Check if they are authorised to EDIT the category
            category = session.query(Category).filter_by(id=category_id).one()
            category_owner = category.user_id
            user = session.query(User).filter_by(email=login_session['email']).one()
            user_id = user.id
            if category_owner != user_id:
                return render_template("unAuthorisedEntry.html", STATE=state)
            # If they are, redirect to this
            category_name = category.name
            return render_template('deleteCategory.html', category_id=category_id, category_name=category_name, STATE=state)
        except KeyError:
            return render_template("unAuthorisedEntry.html", STATE=state)
    else:
        deletedCategory = session.query(Category).filter_by(id=category_id).one()
        session.delete(deletedCategory)
        session.commit()
        return redirect(url_for('showCatalog'))


# PROTECTED
@app.route('/catalog/<int:category_id>')
@app.route('/catalog/<int:category_id>/items')
def showItems(category_id): # READ
    state = generateState(login_session, 'state')
    # have an accordian here to expand details
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('showItems.html', items=items, category_id=category_id, STATE=state)


# PROTECTED
@app.route('/catalog/<int:category_id>/items/new', methods=['GET', 'POST'])
def newItem(category_id): # CREATE
    state = generateState(login_session, 'state')
    if request.method == 'GET':
        try:
            user = login_session['username']
            return render_template('newItem.html', category_id=category_id, STATE=state)
        except KeyError:
            return render_template("unAuthorisedEntry.html", STATE=state)
    else:
        user = session.query(User).filter_by(email=login_session['email']).one()
        user_id = user.id
        category = session.query(Category).filter_by(id=category_id).one()
        # Double check that user is authorised to make an item in this category
        if category.user_id != user_id:
            return render_template("unAuthorisedEntry.html", STATE=state)
        newItem = Item(title=request.form['title'], description=request.form['description'], category_id=category_id, user_id=user_id)
        session.add(newItem)
        session.commit()
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
            return render_template('editItem.html', categories=categories, category_id=category_id, item_id=item_id, item_name=item_name, STATE=state)
        except KeyError:
            return render_template("unAuthorisedEntry.html", STATE=state)
    else:
        user = session.query(User).filter_by(email=login_session['email']).one()
        user_id = user.id
        # Double check that user is authorised to make an item in this category
        if editedItem.user_id != user_id:
            return render_template("unAuthorisedEntry.html", STATE=state)
        # Update values
        editedItem.title = request.form['title']
        editedItem.description = request.form['description']
        category_id = request.form['category_id']
        editedItem.category_id = category_id
        session.add(editedItem)
        session.commit()
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
             return render_template("unAuthorisedEntry.html", STATE=state)
    else:
        user = session.query(User).filter_by(email=login_session['email']).one()
        user_id = user.id
        # Double check that user is authorised to make an item in this category
        if deletedItem.user_id != user_id:
            return render_template("unAuthorisedEntry.html", STATE=state)
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('showItems', category_id=category_id))

# need to add JSON endpoints and login button
# also need to add login protection over certain pages

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
