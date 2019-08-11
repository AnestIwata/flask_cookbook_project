from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SelectMultipleField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User, Category, Country, Cuisine

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
    country = QuerySelectField(u'Country you are from', query_factory=Country.get_all_countries, get_label='name')
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
    ingredients = SelectMultipleField('Select ingredients', coerce=int, validators=[DataRequired()])
    allergens = StringField('Select allergens', validators=[DataRequired()])
    image = FileField('Upload your image: ', validators=[FileRequired()])
    cuisine = QuerySelectField(u'Choose cuisine', query_factory=Cuisine.get_all_cuisines, get_label='name')
    category = QuerySelectField(u'Choose category', query_factory=Category.get_all_categories, get_label='name')
    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message: ', validators=[Length(min=10, max=5000)])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    category = SelectField('Category', coerce=int, validators=[DataRequired()], id='select_category')
    ingredients = SelectField('Ingredients', coerce=int, validators=[DataRequired()], id='select_cuisine')
    any_ingredients = SelectField('Recipe needs to have', coerce=int, validators=[DataRequired()], id='select_cuisine')
    allergens = SelectField('Allergens', coerce=int, validators=[DataRequired()], id='select_allergens')
    search_text = StringField()
    submit = SubmitField('Search Recipes')


