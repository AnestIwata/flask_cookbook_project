from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')

class RecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired()])
    content = TextAreaField('Your recipe instructions: ', validators=[Length(min=50, max=5000)])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    allergens = StringField('Allergens', validators=[DataRequired()])
    cuisine = SelectField('Cuisine', coerce=int, choices= [(1,'American'), (2, 'Mexican')], validators=[DataRequired()], id='select_cuisine')
    country = SelectField('Country you are from', coerce=int, choices= [(1,'USA'), (2, 'Mexico')], validators=[DataRequired()], id='select_country')
    submit = SubmitField('Submit')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message: ', validators=[Length(min=10, max=5000)])
    submit = SubmitField('Submit')
