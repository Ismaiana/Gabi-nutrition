
from flask import Flask, render_template, redirect, flash, session, url_for, request
from model import connect_to_db, db
from passlib.hash import argon2
from jinja2 import StrictUndefined
import os
import crud


app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined
app.secret_key = os.environ["secret_key"]
connect_to_db(app)



@app.route('/')
def homepage():
    """Display homepage."""

    return render_template("index.html")


@app.route('/consultoria')
def consultoria():
    """Display programs' page"""

    return render_template("consultoria.html")




@app.route('/review-my-services-consultoria-gbsilva')
def reviews():
    """Display review form page"""

    return render_template("review_form.html")


@app.route('/thank_you')
def thanks():
    """Display thank you page"""

    return render_template("thankyou.html")


@app.route('/review_me', methods=['POST'])
def create_review():
    """Create a new review to db"""


    user_email = request.form.get('email_db')
    fname = request.form.get('fname_db')
    lname = request.form.get('lname_db')
    review = request.form.get('review-text')



    review = crud.create_review(user_email, fname, lname, review)
    db.session.add(review)
    db.session.commit()
    

    return redirect("/thank_you")

@app.route('/resultados')
def display_reviews():
    """Display reports forum"""


    reviews = crud.get_reviews()


    return render_template('results.html', reviews=reviews)

@app.route('/login-admin')
def login():
    """Display login page"""

    return render_template('login')


@app.route('/login', methods=['POST'])
def login_form():
    """Process user login"""

    email = request.form.get('email')
    password = request.form.get('password')
    
    user = crud.get_user_by_email(email)
    
   
    if not user or not argon2.verify(password, user.password):

        flash('The email or password you entered was incorrect.')

        return redirect('/login-admin')
        
    else:

        session['user_email'] = user.email
       

        return redirect('/')
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)