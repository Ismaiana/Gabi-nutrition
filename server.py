
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
    


@app.route('/logout', methods=['GET','POST'])
def process_logout():
    """Log out user in session"""

    request.form.get('logout')

    session['user_email']

    session.pop('user_email', None)
    flash('Logged out.')
    
    return redirect('/login-admin')

    

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


@app.route('/delete_review')
def delete_review():
    """Button to delete review"""



    button_delete = request.args.get('delete_review')
        
    remove_review = crud.get_review_by_id(button_delete)
  

    if remove_review:
        db.session.delete(remove_review)
        db.session.commit()

    return redirect('/resultados') 

@app.route('/delete-photo')
def delete_photo():
    """Delete photo"""

    button_delete_pic = request.args.get('delete-photo')

    remove_photo = crud.get_photo(button_delete_pic)

    if remove_photo:
        db.session.delete(remove_photo)
        db.session.commit()
    
    return redirect('/resultados') 



   


    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)