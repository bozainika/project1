from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_
from werkzeug.security import generate_password_hash, check_password_hash 
from sqlalchemy.dialects.mysql import ENUM


#setting database variable:
db=SQLAlchemy()

#===============================================================================

class User(db.Model):

    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    passwrd = db.Column(db.LargeBinary, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    #user_reviews= db.relationship("Review", backref="user_reviews", lazy=True)

    def __init__(self, username, passwrd, email):

        self.username=username
        self.passwrd=generate_password_hash(passwrd).encode('utf-8')
        self.email=email

    def register(self):
        '''Add the User object to the database'''
        db.session.add(self)
        db.session.commit()

    def log_in(username_,passwrd_):
        '''Check for a record with username_ and pasword_
        return None if there is no record, else return User object'''
        user = User.query.filter_by(username=username_).first()
        if user == None:
            return None
        user.passwrd=user.passwrd.decode('utf-8')
        if not check_password_hash(user.passwrd,passwrd_):
            return None
        else:
            return user

    def get_user(id_):
        return User.query.get(id_);

#===============================================================================

class Review(db.Model):
    """docstring for Review"""
    __tablename__='reviews'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable = False)
    rate = db.Column('rate', ENUM('1','2','3','4','5'))
    review = db.Column(db.String(500), nullable=False)
    parent_book = db.relationship("Book", backref=db.backref("book_revs"))
    by_user = db.relationship("User",backref="user_revs")

    def __init__(self,user_id,book_id, review, rate=None):
        self.user_id=user_id
        self.book_id=book_id
        self.rate=rate
        self.review=review

    def create_review(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False
        return True


#=======================================================================================

class Book(db.Model):
    __tablename__='books'
    isbn = db.Column(db.String(20), unique=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.SmallInteger,nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #book_revs = db.relationship("Review", backref="parent_book", lazy=True)

    def get_books(keyword):
        result=Book.query.filter(or_((Book.isbn.like("%{}%".format(keyword))),
                                     (Book.title.like("%{}%".format(keyword))),
                                     (Book.author.like("%{}%".format(keyword))))).all()

        return result

    def get_book_by_isbn(isbn_):
        result=Book.query.filter_by(isbn=isbn_).first()
        
        return result
        

