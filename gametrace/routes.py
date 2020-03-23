import os
import secrets
from PIL import Image
from flask import Flask, request, render_template, url_for, flash, redirect
from gametrace import app, db, bcrypt
from gametrace.forms import RegistrationForm, LoginForm, UpdateAccountForm
from gametrace.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required


# Unique=True means that only one user can own the specific password, username, etc..
# nullable=True means that the specified field can be empty/none/null

test_data = [
    {
        "user": "Brock",
        "status": "Last played Diablo 3",
        "announcement": "Unlocked new item",
        "details": "Flaming shark spear!"
    },
    {
        "user": "Ash",
        "status": "Last played Call of Duty",
        "announcement": "Leveled up! Now level 50",
        "details": "Flaming shark spear!"
    }
]

@app.route('/')
def home():
    # title = "home"
    # name = request.args.get("name", "World")
    # return f'Hello, {escape(name)}!'
    return render_template("index.html", test_data=test_data, title="Home")

@app.route('/info')
def info():
    return render_template("info.html", test_data=test_data, title="Info")
# $ env FLASK_APP=hello.py flask run
#  * Serving Flask app "hello"
#  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
        # If user exists and password they entered is valid, we want to log the user in...
            login_user(user, remember=form.remember.data)
            # If user checks 'remember me' ==> remember=True, else ==> remember=False
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            # Redirect to the next page, if next page exists. If it is none or false, redirect to home page
        else:
            flash('Login unsuccessful. Please check the email and password', 'danger') 
        # We filter any users with the same email just entered...
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Image resizing
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)