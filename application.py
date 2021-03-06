import os

from flask import Flask, request, session
from flask import render_template as rt
from flask_session import Session

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from Models import *

#==================================================================================
#setting up flask application
app=Flask(__name__)

#configuring session variables
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#==================================================================================

#configuring database session variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#==================================================================================

def post(var):
	'''Get var from the POST array'''

	return request.form.get(var)

#==================================================================================

@app.route("/")
def index(status=None):
	''' Displays home page if user is logged in or
	 redirect him to the log in page '''
	
	if session["id"] == None:
		return rt('lf.html', status='You must log in')
	
	else:
		return rt('index.html', status=status)

#==================================================================================

@app.route("/rf")
def rf(status= None):
	''' Displays registration page if user is not logged in or
	 redirect him to the home page '''
	
	if session["id"]==None: 
		return rt('rf.html', status=status)
	
	else:
		return rt('index.html', status=status)

#==================================================================================

@app.route("/lf" )
def lf(status = None):
	''' Displays log in page if user is not logged in or redirect him to the home page '''

	if session['id']==None: 
		return rt('lf.html', status=status)

	else: return rt('index.html', status=status)

#==================================================================================

@app.route('/reg',methods=["POST"])
def register():
    ''' Register user in the database and redirect him to the log in page'''
    if post('password')==post('confirm'):
        try:
            user=User(username=post('username'), passwrd=post('password'), email=post('email'))
            user.register();
        except IntegrityError:
            db.session.rollback()
            return rt('rf.html', status='The username or email you are trying to used are not available')
        else:
            return rt('lf.html', status='success')
 
#==================================================================================

@app.route('/login',methods=['POST'])
def login():
	''' Log in user and redirect him to the home page, set session[id]=user.id '''

	user=User.log_in(post('username'),post('password'))
	if user != None:
		session['id']=user.id
		return rt('index.html', status='You logged in successfully', user=session['id'])
	else: 
		return rt('lf.html',status="danger")

#==================================================================================

@app.route('/books/page<int:page>')
def books(page):
	''' Display 25 books on each page from a database if user is logged in '''
	if not session['id']:
		return rt('lf.html', status='You must log in')
	books_objects=Book.query.all()
	last = Book.query.order_by(Book.id.desc()).first().__dict__
	books=[]
	for i in range (((page-1)*25),(page*25)):
		try:
			book=books_objects[i]
			book=book.__dict__
			books.append(book)
		except Exception:
			break;
	return rt('show_books.html', books=books, page=page, last=last)
#==================================================================================

@app.route('/search',methods=['GET'])
def search_page():
    '''Display 25 books on each page from the search results if user is logged in'''
    if not session['id']:
        return rt('lf.html', status='You must log in')
    search=str(request.args.get('search'))
    results=Book.get_books(search)
    books=[]
    if results:
        for res in results:
            try:
                book=res
                book=book.__dict__
                books.append(book)
            except Exception:
                break;
        return rt('book.html', books=books)
    else:return rt('index.html', status='No matches')

#==================================================================================

@app.route('/logout')
def logout():
	'''Log out user by setting session[id] to be None and redirect to Log in page''' 

	session['id']=None
	return rt('lf.html',status='You logged out')

#==================================================================================

@app.route('/details/<string:isbn>')
def details(isbn,status=None):
    book=Book.get_book_by_isbn(isbn)
    if not book:
        return 'no such book'
    reviews=book.book_revs
    
    if reviews: 
        count_0s=0
        avg_rate=0
        for r in reviews:
            if r.rate:
                avg_rate+=float(r.rate)
            else:
                count_0s+=1
        avg_rate=avg_rate/(len(book.book_revs)-count_0s)
        avg_rate=str("%.2f"%avg_rate)
        return rt('book_details.html',avg_rate=avg_rate, book=book, status=status)
    else:
        return 'no revs'

#================================================================================================

@app.route('/details/post', methods=['POST'])
def post_comment(status=None):
    
    book=Book.get_book_by_isbn(post('isbn'))
    review=Review(user_id=session['id'],book_id=book.id,review=post('content'), rate=post('rate'))
    
    if review.create_review():
        avg_rate=0
        count_0s=0
        for r in book.book_revs:
            if r.rate:
                avg_rate+=float(r.rate)
            else:
                count_0s+=1
        avg_rate=avg_rate/(len(book.book_revs)-count_0s)
        avg_rate=str("%.2f"%avg_rate)
        status='You created review'
        return rt('book_details.html',avg_rate=avg_rate, book=book, status=status)
    else:
        avg_rate=0
        for r in reviews:
            if r.rate:
                avg_rate+=float(r.rate)
        avg_rate=avg_rate/len(reviews)
        status='Could not create a review'
        return rt('book_details.html',avg_rate=avg_rate, book=book, status=status)
    


def main():
  

    if __name__ =="__main__":
        with app.app_context():
            main()




