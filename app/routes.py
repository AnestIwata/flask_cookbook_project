import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RecipeForm, ContactForm, RegistrationForm, SearchForm
from app.models import Recipe, User, Ingredient, Country, Category, Allergen
from app.poppulate_database import Poppulate

# Homepage route
@app.route('/')
@app.route('/index')
def index():
    Poppulate.poppulate_database()
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
        return render_template('index.html', title='Sign In', form=form)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, 
            email=form.email.data,
            country=form.country.data
            )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congrats, you are now a registered user!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/add_recipe', methods=["GET", "POST"])
def add_recipe():
    if current_user.is_authenticated:
        form = RecipeForm()
        form.ingredients.choices = db.session.query(Ingredient.id, Ingredient.name).all()
        form.ingredients.countries = db.session.query(Country.id, Country.name).all()
        if form.validate_on_submit():
            # db_ingredients = []
            # for ingredient in form.ingredients.data:
            #     db_ingredients.append(Ingredient.query.filter_by(id=ingredient))
            f = form.image.data
            filename = secure_filename(f.filename)
            print(filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(file_path)
            f.save(file_path)

            recipe = Recipe(
                name=form.name.data, 
                content=form.content.data, 
                cuisine=form.cuisine.data,
                category=form.category.data,
                # ingredients=form.ingredients.data,
                # allergens=form.allergens.data,
                image="static/img/recipes_images/" + filename,
                author=current_user
            )
            # f = form.image.data
            db.session.add(recipe)
            db.session.commit()
            flash("Congrats, you have added a recipe!")
            return redirect(url_for('recipes_list'))
    else:
        flash("You need to login before you add recipe.")
        return redirect(url_for('login'))
    return render_template("add_recipe.html", title='Add Recipe', form=form)

@app.route('/recipe/<recipe_name>')
def recipe(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first_or_404()
    return render_template("recipe.html", recipe=recipe)

@app.route('/recipes_list', methods=["GET", "POST"])
def recipes_list():
    form = SearchForm()
    recipes = Recipe.query.all()
    ingredients = Ingredient.query.all()
    categories = Category.query.all()
    first_three_ingredients = Ingredient.query.limit(3).all()
    allergens = Allergen.query.all()
    # Recipe.query.filter(Recipe.ingredients.any(name="wheat flour")).all()

    return render_template("recipes_list.html", title='Recipes', recipes=recipes, categories=categories, 
                            ingredients=ingredients, first_three_ingredients=first_three_ingredients, allergens=allergens)

@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    return render_template("contact.html", form=form)
