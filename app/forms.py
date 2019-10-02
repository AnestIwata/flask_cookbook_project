from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SelectMultipleField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField, widgets
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo, NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import User, Category, Country, Cuisine, Recipe


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

class EditForm(FlaskForm):
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

    def __init__(self, original_name, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            recipe = Recipe.query.filter_by(name=self.name.data).first()
            print(recipe)
            if recipe is not None:
                print(str(name.data) + " " + str(self.original_name))
                raise ValidationError('Please use a different name.')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message: ', validators=[Length(min=10, max=5000)])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    comment = TextAreaField('Comment: ', validators=[
                            Length(min=5, max=5000)])
    website = StringField('Website')
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    cuisine = QuerySelectField(
        u'Choose cuisine:', query_factory=Cuisine.get_all_cuisines, get_label='name',
        render_kw={'class':'form-control js-search-category select2-hidden-accessible'})
    category = QuerySelectField(
        u'Choose category:', query_factory=Category.get_all_categories, get_label='name',
        render_kw={'class':'form-control js-search-category select2-hidden-accessible'})
    ingredients = SelectMultipleField(
        'Select ingredients (you can select more than one):', coerce=int,
        render_kw={'class':'form-control js-search-category select2-hidden-accessible', 'multiple':'multiple'})
    allergens = SelectMultipleField(
        'No allergens (you can select more than one):', coerce=int,
        render_kw={'class':'form-control js-search-category select2-hidden-accessible', 'multiple':'multiple'})
    any_ingredients = SelectField('Recipe needs to have', coerce=int, 
        render_kw={'class':'form-control js-search-category select2-hidden-accessible'})
    sortkey = SelectField('Sort recipes by: ')
    submit = SubmitField('Search Recipes')

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)

