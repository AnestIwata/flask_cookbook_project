import os
import re
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
    recipes = Recipe.query.limit(3).all()
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
        form.ingredients.choices = db.session.query(
            Ingredient.id, Ingredient.name).all()
        form.allergens.choices = db.session.query(
            Allergen.id, Allergen.name).all()
        if form.validate_on_submit():
            f = form.image.data
            filename = secure_filename(f.filename)
            file_path = os.path.join(
                "app/static/img/recipes_images",  filename)
            f.save(file_path)

            recipe = Recipe(
                name=form.name.data,
                content=form.content.data,
                cuisine=form.cuisine.data,
                category=form.category.data,
                time_to_prepare=form.time_to_prepare.data,
                serves_num_people=form.serves_num_people.data,
                cooking_time=form.cooking_time.data,
                image="static/img/recipes_images/" + filename,
                author=current_user
            )

            ingredients_in_recipe = []
            for ingredient in form.ingredients.data:
                queried_ingredient = Ingredient.query.filter_by(
                    id=ingredient).first()
                ingredients_in_recipe.append(queried_ingredient)
            recipe._ingredients = ingredients_in_recipe

            allergens_in_recipe = []
            for allergen in form.allergens.data:
                queried_allergen = Allergen.query.filter_by(
                    id=allergen).first()
                allergens_in_recipe.append(queried_allergen)
            recipe._allergens = allergens_in_recipe

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
    content = re.split(r' *[\.\?!][\'"\)\]]* *', recipe.content)
    short_summary = content[0]
    return render_template("recipe_page.html", recipe=recipe, content=content, short_summary=short_summary)


@app.route('/recipes_list', methods=["GET", "POST"])
def recipes_list():
    form = SearchForm()
    recipes = Recipe.query.limit(9).all()
    ingredients = Ingredient.query.all()
    categories = Category.query.all()
    first_three_ingredients = Ingredient.query.limit(3).all()
    allergens = Allergen.query.all()
    # if form.validate_on_submit():

    # Recipe.query.filter(Recipe.ingredients.any(name="wheat flour")).all()

    return render_template("recipes_list.html", title='Recipes', form=form, recipes=recipes, categories=categories,
                           ingredients=ingredients, first_three_ingredients=first_three_ingredients, allergens=allergens)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    return render_template("contact.html", form=form)


@app.route('/search_handler', methods=["POST"])
def search_handler():
    category_form = request.form.get('category')
    ingredients_form = request.form.getlist('ingredients[]')
    allergens_form = request.form.getlist('allergens[]')
    choose_ingredients = request.form.get('choose_ingredients')
    queried_recipes = []
    if category_form != 1:
        queried_recipes = Recipe.query.filter_by(
            category_id=category_form).all()
        if ingredients_form != []:
            for ingredient in ingredients_form:
                temp_recipes = Recipe.query.filter(
                    Recipe._ingredients.any(Ingredient.name == ingredient)).all()
                queried_recipes = list(
                    set(queried_recipes).intersection(temp_recipes))
        if allergens_form != []:
            for allergen in allergens_form:
                temp_recipes = Recipe.query.filter(
                    Recipe._allergens.any(Allergen.name == allergen)).all()
                queried_recipes = list(
                    set(queried_recipes).intersection(temp_recipes))

    queried_recipes = list(set(queried_recipes))
    form = SearchForm()
    ingredients = Ingredient.query.all()
    categories = Category.query.all()
    first_three_ingredients = Ingredient.query.limit(3).all()
    allergens = Allergen.query.all()
    return render_template("recipes_list.html", title='Recipes', form=form, recipes=queried_recipes, categories=categories,
                           ingredients=ingredients, first_three_ingredients=first_three_ingredients, allergens=allergens)
