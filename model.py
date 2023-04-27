"""Model for Gabi website"""


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User model for website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Reviews review_id={self.user_id} user_email={self.email} password={self.password}>'



class Reviews(db.Model):
    """Reviews for reviews page"""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_email = db.Column(db.String, unique=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    review = db.Column (db.String(350))

    def __repr__(self):
        return f'<Reviews review_id={self.review_id} user_email={self.user_email} fname={self.fname} lname={self.lname} review={self.review}>'

def connect_to_db(flask_app, db_uri="postgresql:///reviews", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    app.app_context().push()
    db.create_all()