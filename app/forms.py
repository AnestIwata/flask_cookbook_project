from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RecipeForm(FlaskForm):
    name = StringField('Recipe Name', validators=[DataRequired()])
    content = TextAreaField('Your recipe instructions: ', validators=[Length(min=0, max=500)])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    allergens = StringField('Allergens', validators=[DataRequired()])
    cuisine = SelectField('Cuisine', coerce=int, choices= [(1,'American'), (2, 'Mexican')], validators=[DataRequired()], id='select_cuisine')
    country = SelectField('Country you are from', coerce=int, choices= [(1,'USA'), (2, 'Mexico')], validators=[DataRequired()], id='select_country')

    submit = SubmitField('Submit')