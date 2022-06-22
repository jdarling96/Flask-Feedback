
from crypt import methods
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import *
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Redirects to /register"""
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Create a new user"""
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first = form.first_name.data
        last = form.last_name.data
        
        new_user = User.register(username,password,email,first,last)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.email.errors.append('Email in use. Please choose another.')
            return render_template('register.html', form=form)    

        session['user_login'] = new_user.username
        flash(f'Welcome, {new_user.username}!', 'success')
        return redirect(f'/users/{new_user.username}')

    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    """Login form for user"""
    form = LoginForm()
    

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome back, {user.username}!', 'success')
            session['user_login'] = user.username
            return redirect(f'/users/{user.username}')
        else:
              form.username.errors = ['Invalid username/password']
              return redirect('/')  

    return render_template('login.html', form=form)

@app.route('/users/<string:username>')
def secret_page(username):
    """Users info page that can only be accesed by user"""
    user = User.query.get_or_404(username)
    if 'user_login' not in session:
        flash('You must log-in first!', 'warning')
        return redirect('/')

    return render_template('user_info.html', user=user) 

@app.route('/logout')
def logout_user():
    """Logs user out and removes them from the session"""
    session.pop('user_login')
    flash('Goodbye!', 'info')
    return redirect('/')  

@app.route('/users/<string:username>/delete', methods=['POST'])
def delete_user(username):
    """Removes user from session and deletes all feedback"""
    user = User.query.get_or_404(username)
    if session['user_login'] != user.username:
        flash('You', 'warning')
        return redirect('/')         