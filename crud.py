"""Crud functions"""

from model import db, Reviews, connect_to_db


def create_review(user_email, fname, lname, review):

    review = Reviews(user_email=user_email, fname=fname, lname=lname, review=review)

    return review

def get_reviews():
    

    return Reviews.query.all()


def get_review_by_id(review_id):
    

    return Reviews.query.get(review_id)


def get_review_by_email(user_email):
   

    return Reviews.query.filter(Reviews.user_email == user_email).first()

if __name__ == '__main__':
    from server import app

    connect_to_db(app)