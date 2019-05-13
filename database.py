from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

engine=create_engine(os.getenv('DATABASE_URL'))
db=scoped_session(sessionmaker(bind=engine))

def register_user(username,password,confirm,email):
    '''
    register_user(username,password,confirm,email)
    Creates sql alchemy connection and scope session 
    and check if password and confirm match if not return error string
    then check for a row that matches the username or email
    and if it does it returns an error string, otherwise instert the 
    data into the database and return 'success' 

    '''
    
    if not password == confirm:
        return "Passwords do not match"

    res=db.execute("SELECT id FROM users WHERE username=:u OR email=:e",{"u":username,"e":email})
    if res==None: #check if the query was executed properly, if there is a returned object 
        return "Can\'t create new user"


    if res.rowcount==0:
        if db.execute("INSERT INTO users (username,pass,email) VALUES (:username, AES_ENCRYPT(:password,'secret'), :email)", 
            {"username":username,"password":password,"email":email}):
            db.commit(); #important line!!!
            return 'success'
        else:
            return "Can\'t create new user"
    else:
        return "User already exists"

#====================================================================================================================================

def login_user(username,password):
    ''' login_user(username,password) 
    Creates sql alchemy connection and scope session 
    and check for a record with row that matches 
    both username and password and returns users' ID 
    or string with '1' if it fails to connect to db
    and string with '2' if there is no record '''

    if engine == None or db == None : 
        return '1'

    user=db.execute("SELECT id FROM users WHERE username=:username AND pass=AES_ENCRYPT(:password,'secret')",
        {'username':username,'password':password}).fetchone()
    db.commit()
    if user==None:
        return '3'
    else:
        return user

#====================================================================================================================================

def list_books():
    ''' Gives a full list of the books in a database '''
    books=db.execute("SELECT * FROM books").fetchall()
    db.commit()
    return books

#====================================================================================================================================

def post(var):
    return request.form.get(var)

#====================================================================================================================================

def get_book(isbn):
    pass