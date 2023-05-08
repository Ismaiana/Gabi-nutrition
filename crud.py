"""Crud functions"""

from model import db, Reviews, User, Photos, connect_to_db


def create_review(user_email, fname, lname, review):

    review = Reviews(user_email=user_email, fname=fname, lname=lname, review=review)

    return review

def get_reviews():
    

    return Reviews.query.all()


def get_review_by_id(review_id, review):
    

    return Reviews.query.filter_by(review_id = review_id, review=review).first()


def get_review_by_email(user_email):
   

    return Reviews.query.filter(Reviews.user_email == user_email).first()


def get_user_by_email(email):
   

    return User.query.filter(User.email == email).first()

def upload_photo(user_id, filename):

    photo= Photos(user_id=user_id, filename=filename)

    return photo

def get_all_photos():

    return Photos.query.all()



if __name__ == '__main__':
    from server import app

    connect_to_db(app)