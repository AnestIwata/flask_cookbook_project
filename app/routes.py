from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.forms import LoginForm, RecipeForm, ContactForm, RegistrationForm, SearchForm
from app.models import Recipe, User, Ingredient
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.poppulate_database import Poppulate

# Homepage route
@app.route('/')
@app.route('/index')
def index():
    recipes = Recipe.query.all()
    return render_template("index.html", recipes=recipes)

# Login page route
@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/add_recipe', methods=["GET", "POST"])
def add_recipe():
    Poppulate.poppulate_database()
    form = RecipeForm()
    # Change this to current user.
    user = User(username="Frank", email="frank@ma.com", password_hash="sads", country="Poland")
    form.ingredients.choices  = db.session.query(Ingredient.id, Ingredient.name).all()
    if form.validate_on_submit():
        db_ingredients = []
        for ingredient in form.ingredients.data:
            db_ingredients.append(Ingredient.query.filter_by(id=ingredient))

        recipe = Recipe(
            name=form.name.data, 
            content=form.content.data, 
            # ingredients=db_ingredients,
            # allergens=form.allergens.data,
            author=user,
            cuisine=form.cuisine.data,
        )
        db.session.add(recipe)
        db.session.commit()
        flash("Congrats, you have added a recipe!")
        return redirect(url_for('recipes_list'))
    return render_template("add_recipe.html", title='Add Recipe', form=form)

@app.route('/recipe/<recipe_name>')
def recipe(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first_or_404()
    return render_template("recipe.html", recipe=recipe)

@app.route('/recipes_list')
def recipes_list():
    form = SearchForm()
    recipes = Recipe.query.all()
    return render_template("recipes_list.html", title='Recipes', recipes=recipes)

@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    return render_template("contact.html", form=form)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    return render_template("register.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)

