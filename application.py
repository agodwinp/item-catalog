from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, make_response, abort, g
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User, Category, Item
from flask_httpauth import HTTPBasicAuth
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random, string, json, requests, httplib2

app = Flask(__name__)
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread':False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']

# fake data
user = {'id':1, 'username':'arungp', 'password_hash':'pa55W0rd'}
users = [{'id':1, 'username':'arungp', 'password_hash':'pa55W0rd'}, {'id':2, 'username':'arungp2', 'password_hash':'pa55W0rd2'}]
category = {'id':1, 'name':'Football'}
categories = [{'id':1, 'name':'Football'}, {'id':2, 'name':'Basketball'}]
item = {'id':1, 'title':"Boots", "description":"This is the description", "category_id":1}
items = [{'id':1, 'title':"Boots", "description":"This is the description", "category_id":1}, {'id':2, 'title':"Gloves", "description":"This is the description", "category_id":1}]


# verify authorisation
@auth.verify_password
def verify_password(username_or_token, password):
    # attempt verification with token
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    # otherwise, try username
    else:
        user = session.query(User).filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/')
def home(): # READ
    return render_template("home.html")

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template("login.html", STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/catalog')
def showCatalog(): # READ
    return render_template('allCategories.html', categories=categories)

# PROTECTED
@app.route('/catalog/new', methods=['GET', 'POST'])
def newCategory(): # CREATE
    return "This page will create a new category"

# PROTECTED
@app.route('/catalog/<string:category_name>/edit', methods=['GET', 'POST'])
def editCategory(category_name): # UPDATE
    return "This page will edit a category"

# PROTECTED
@app.route('/catalog/<string:category_name>/delete', methods=['GET','POST'])
def deleteCategory(category_name): # DELETE
    return "This page will delete a category"

# PROTECTED
@app.route('/catalog/<string:category_name>')
@app.route('/catalog/<string:category_name>/items')
def showItems(category_name): # READ
    # have an accordian here to expand details
    info = []
    for i in items:
        data = {}
        data['name'] = i['title']
        data['description'] = i['description']
        category_id = i['category_id']
        for j in categories:
            if j['id'] == category_id:
                data['category'] = j['name']
        info.append(data)
    return render_template('showItems.html', info=info)

@app.route('/catalog/<string:category_name>/items/<string:item_name>')
def showItemDetails(category_name, item_name): # READ
    return "This page will show the item details for a category"

# PROTECTED
@app.route('/catalog/<string:category_name>/items/new', methods=['GET', 'POST'])
def newItem(category_name): # CREATE
    return "This page will create new item for a category"

# PROTECTED
@app.route('/catalog/<string:category_name>/items/<string:item_name>/edit')
def editItem(category_name, item_name): # UPDATE
    return "This page will edit an item for a category"

# PROTECTED
@app.route('/catalog/<string:category_name>/items/<string:item_name>/delete')
def deleteItem(category_name, item_name): # DELETE
    return "This page will delete an item for a category"

# need to add JSON endpoints and login button
# also need to add login protection over certain pages

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
