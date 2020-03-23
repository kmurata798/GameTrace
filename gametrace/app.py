from datetime import datetime
from flask import Flask, escape, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '1e51fab5a353df7272058fda03dd063b'
# SQLAlchemy is a database!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Unique=True means that only one user can own the specific password, username, etc..
# nullable=True means that the specified field can be empty/none/null
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    image_file = db.Column(db.String(25), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # Referencing the Post Class
    posts = db.relationship('Post', backref='author', lazy=True)
    # In posts field, 'backref' is similar to adding another column to the Post model.
    # This is how we do ONE TO MANY for users and posts. We can find who made a post by using 'author'

    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # Referencing the table name/column name
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

if __name__== '__main__':
    app.run()(debug=True)