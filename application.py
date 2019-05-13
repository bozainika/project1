from flask import Flask, session
from flask import render_template as rt
from flask_session import Session

import os

from database import register_user, login_user, list_books, post #, get_book 

#==================================================================================

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
	raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#==================================================================================

@app.route("/")
def index(status=None):
	
	if session['id'] == None:
		return rt('lf.html', status='You must log in')
	
	else:
		return rt('index.html', status=status)

#==================================================================================

@app.route("/rf")
def rf(status= None):
	
	if session['id']==None: return rt('rf.html', status=status)
	
	else: return rt('index_logged.html', status=status)
	

@app.route("/lf" )
def lf(status = None):
	return rt('lf.html', status=status)

#==================================================================================

@app.route('/reg',methods=["POST"])
def register():
	
	status=register_user(post('username'), post('password'),post('confirm'), post('email'))
	#post(var) self made function to get the value from POST[var]
	
	if status=='success':
		return rt('lf.html',status=status)
	else:
		return rt('rf.html', status=status) 

#==================================================================================

@app.route('/login', methods=["POST"])
def login(status=None):

	value=login_user(post('username'), post('password'))
	
	if value=='1' or value=='2' or value=='3':
		return rt('lf.html', status='danger', err=value)
	
	session['id']=value['id']
	return rt('index.html', status='You logged in successfully', user=session['id'])

#==================================================================================

@app.route('/books')
def books():
	return rt('book.html',books=list_books())

#==================================================================================

@app.route('/logout')
def logout():
	session['id']=None
	return rt('lf.html',status='You logged out')

#==================================================================================

@app.route('/details/<string:isbn>')
def details(isbn):
	pass
