
from flask import Flask, render_template, redirect, flash, session, url_for, request
from model import connect_to_db, db
from werkzeug.utils import secure_filename
from passlib.hash import argon2
from jinja2 import StrictUndefined
import secrets
import os
import crud
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined
app.secret_key = os.environ["secret_key"]
app.SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
app.config['UPLOAD_FOLDER'] = 'static/img'
connect_to_db(app)

reset_tokens = {}

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

@app.route('/register')
def new_user():
    """Display form to create a new user"""


    return render_template('register.html')


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




@app.route('/reset_password', methods=['POST'])
def reset_request():
    """Send email with password request"""

    email = request.form.get('email_db')
    print(email)
    user = crud.get_user_by_email(email)

    if not user:
        flash('Email did not match our records, try again')
        return redirect('/reset_password')

    else:
        
        token = secrets.token_urlsafe(32)
        
        reset_tokens[email] = token
        flash('Link to reset password sent to your email')
        message = Mail(
        from_email='no-reply-reset-password-website-gcoachsilva@hotmail.com',
        to_emails= email,
        subject='Reset your Password',
        html_content=f'<strong>Hello,<br>To reset your password, just click the link below.</strong> \
        <a href="{url_for("password_request_form", email=email, token=token, _external=True)}"><br>Reset Password</a>')
        try:
            sg = SendGridAPIClient(os.environ.get(app.SENDGRID_API_KEY))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

        return redirect('/login-admin')
    
@app.route('/reset_password')
def reset_form():
    """Form reset password request"""


    return render_template('reset_password.html')


@app.route('/process_request_password', methods=['POST'])
def new_password():
    """Collect new password for db"""
    email = session['user_email']
    new_password = request.form.get('new-password')
    confirm_password = request.form.get('confirm-password')
    user = crud.get_user_by_email(email)

    hashed = argon2.hash(confirm_password)

    if new_password == confirm_password:
        new_password_db = crud.reset_password(user.user_id, hashed)
        db.session.add(new_password_db)
        db.session.commit()


        flash('Password updated, please log in')
    return redirect('/login-admin')



@app.route('/process_request_password')
def password_request_form():
    """Display form for password change"""

    email = request.args.get('email')
    token = request.args.get('token')
  
    if email in reset_tokens and reset_tokens[email] == token:
        session['user_email'] = email
        return render_template('new_password.html')
    else:
        flash('Invalid or expired password reset link')
        return redirect('/login-admin')
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)