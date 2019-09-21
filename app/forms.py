from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SelectMultipleField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField, widgets
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo, NumberRange
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
    country = QuerySelectField(
        u'Where are you from?', query_factory=Country.get_all_countries, get_label='name')
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
    name = StringField('Recipe Name:', validators=[DataRequired()])
    content = TextAreaField('Your recipe instructions: ', validators=[
                            Length(min=50, max=5000)])
    ingredients = SelectMultipleField(
        'Select ingredients (you can select more than one):', coerce=int, validators=[DataRequired()],
        render_kw={'class':'form-control js-search-category select2-hidden-accessible', 'multiple':'multiple'})
    allergens = SelectMultipleField(
        'Select allergens (you can select more than one):', coerce=int, validators=[DataRequired()],
        render_kw={'class':'form-control js-search-category select2-hidden-accessible', 'multiple':'multiple'})
    image = FileField('Upload your image: ', validators=[FileRequired()])
    cuisine = QuerySelectField(
        u'Choose cuisine:', query_factory=Cuisine.get_all_cuisines_except_all, get_label='name',
        render_kw={'class':'form-control js-search-category select2-hidden-accessible'})
    category = QuerySelectField(
        u'Choose category:', query_factory=Category.get_all_categories_except_all, get_label='name',
        render_kw={'class':'form-control js-search-category select2-hidden-accessible'})
    time_to_prepare = IntegerField(u'Time it takes to prepare food (input number of minutes):', validators=[
                                   DataRequired(), NumberRange(min=1, max=48)])
    cooking_time = IntegerField(u'How long it takes to cook food (input number of hours):', validators=[
                                DataRequired(), NumberRange(min=1, max=48)])
    serves_num_people = IntegerField(u'How many people can it be served for (input a number):', validators=[
                                     DataRequired(), NumberRange(min=1, max=100)])
    calories = IntegerField(u'Calories:', validators=[DataRequired()])
    carbohydrates = IntegerField(u'Carbohydrates:', validators=[DataRequired()])
    proteins = IntegerField(u'Proteins:', validators=[DataRequired()])
    fats = IntegerField(u'Fats:', validators=[DataRequired()])
    cholesterol = IntegerField(u'Cholesterol:', validators=[DataRequired()])
    submit = SubmitField('Submit')




class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message: ', validators=[Length(min=10, max=5000)])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    cuisine = QuerySelectField(
        u'Choose cuisine:', query_factory=Cuisine.get_all_cuisines_except_all, get_label='name',
        render_kw={'class':'form-control js-search-category select2-hidden-accessible'})
    category = QuerySelectField(
        u'Choose category:', query_factory=Category.get_all_categories_except_all, get_label='name',
        render_kw={'class':'form-control js-search-category select2-hidden-accessible'})
    ingredients = SelectMultipleField(
        'Select ingredients (you can select more than one):', coerce=int,
        render_kw={'class':'form-control js-search-category select2-hidden-accessible', 'multiple':'multiple'})
    allergens = SelectMultipleField(
        'No allergens (you can select more than one):', coerce=int,
        render_kw={'class':'form-control js-search-category select2-hidden-accessible', 'multiple':'multiple'})
    any_ingredients = SelectField('Recipe needs to have', coerce=int, 
        render_kw={'class':'form-control js-search-category select2-hidden-accessible'})
    search_text = StringField()
    submit = SubmitField('Search Recipes')

# class CommentForm(FlaskForm):
    
