from flask import Flask, escape, request, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '1e51fab5a353df7272058fda03dd063b'

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