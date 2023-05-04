
from flask import Flask, render_template, redirect, flash, session, url_for, request
from model import connect_to_db, db
from werkzeug.utils import secure_filename
from passlib.hash import argon2
from jinja2 import StrictUndefined
import os
import crud
import uuid


app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined
app.secret_key = os.environ["secret_key"]
app.config['UPLOAD_FOLDER'] = 'static/img'
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
    """Display photos and reviews"""


    reviews = crud.get_reviews()

    photos = crud.get_all_photos()

    flash('Welcome Admin!')

    return render_template('results.html', reviews=reviews, photos=photos)


@app.route('/login-admin')
def login():
    """Display login page"""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_form():
    """Process user login"""

    email = request.form.get('email')
    password = request.form.get('password')
    
    user = crud.get_user_by_email(email)
    
   
    if not user or password != password:

        flash('The email or password you entered was incorrect.')

        return redirect('/login-admin')
        
    else:

        session['user_email'] = user.email
       
    

        return redirect('/resultados')
    

@app.route('/delete_review')
def delete_review():
    """Button to delete review"""

    user_email = session['user_email']

    review = crud.get_review_by_email(user_email)

    delete_button = request.args.get('review-delete')
    
    remove_review = crud.get_review_by_id(review.review_id)

    db.session.delete(remove_review)
    db.session.commit()

    return redirect('/resultados') #fix this function



@app.route('/upload-photo', methods=['POST'])
def new_photo():
    """Upload new photo"""

    email = session['user_email']
    user = crud.get_user_by_email(email)

    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    upload_photo = crud.upload_photo(user.user_id, filename)
    db.session.add(upload_photo)
    db.session.commit()

    return redirect('/resultados')

   


    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)