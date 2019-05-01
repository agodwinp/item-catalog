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
    return "This will be the home page"

@app.route('/catalog')
def showCatalog(): # READ
    return "This will show all catalog categories"


