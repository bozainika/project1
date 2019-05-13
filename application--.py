from flask import Flask, render_template
from flask_session import Session
import mysql.connector


app=Flask('__name__')

@app.route('/')

def index():
	return 'test1'