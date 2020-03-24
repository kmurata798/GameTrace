import os
import secrets
from PIL import Image
from flask import Flask, request, render_template, url_for, flash, redirect
from gametrace import app, db, bcrypt
from gametrace.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from gametrace.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required


# Unique=True means that only one user can own the specific password, username, etc..
# nullable=True means that the specified field can be empty/none/null
@app.route('/home')
@app.route('/')
def home():
    posts = Post.query.all()
    # Grabbing ALL posts from the DATABASE
    return render_template("index.html", posts=posts, title="Home")

@app.route('/about')
def about():
    return render_template("about.html", title="Info")
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

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # Check if it is a POST request and if it is valid.
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        # Add post to the database
        db.session.commit()
        # Commit changes to the database
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        # Check if it is a POST request and if it is valid.
        post.title = form.title.data
        # Auto-fill title field with existing title
        post.content = form.content.data
        # Auto-fill content field with existing content
        db.session.commit()
        # Commit the changes to the database
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

# @app.route("/post/<int:post_id>/delete", methods=['POST'])
# @login_required
# def delete_post(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your post has been deleted!', 'success')
#     return redirect(url_for('home'))