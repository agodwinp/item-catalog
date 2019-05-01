from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread':False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# fake data
user = {'id':1, 'username':'arungp', 'password_hash':'pa55W0rd'}
users = [{'id':1, 'username':'arungp', 'password_hash':'pa55W0rd'}, {'id':2, 'username':'arungp2', 'password_hash':'pa55W0rd2'}]
category = {'id':1, 'name':'Football'}
categories = [{'id':1, 'name':'Football'}, {'id':2, 'name':'Basketball'}]
item = {'id':1, 'title':"Boots", "description":"This is the description", "category_id":1}
items = [{'id':1, 'title':"Boots", "description":"This is the description", "category_id":1}, {'id':2, 'title':"Gloves", "description":"This is the description", "category_id":1}]


@app.route('/')
def home(): #READ
    return render_template("home.html")

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

@app.route('/catalog/<string:category_name>')
@app.route('/catalog/<string:category_name>/items')
def showItems(category_name): # READ
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
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
