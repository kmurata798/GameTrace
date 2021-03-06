from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
# FileField == type of field it is, FileAllowed == what kind of files we want uploaded validator
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# These imports allow for the creation of forms for the site (Login/Sign up)
from gametrace.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        # if user already exists, then raise error. We don't want duplicate users!
        if user:
            raise ValidationError('That username is already taken. Please try another username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # if user already exists, then raise error. We don't want duplicate users!
        if user:
            raise ValidationError('That email is already taken. Please try another email.')

class LoginForm(FlaskForm):
    # username = StringField('Username',
    #                         validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            # if user already exists, then raise error. We don't want duplicate users!
            if user:
                raise ValidationError('That username is already taken. Please try another username.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            # if user already exists, then raise error. We don't want duplicate users!
            if user:
                raise ValidationError('That email is already taken. Please try another email.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')