import os, re, json 
from datetime import datetime 
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RecipeForm, ContactForm, RegistrationForm, SearchForm
from app.models import Recipe, User, Ingredient, Country, Category, Allergen, Cuisine, NutritionFacts
from app.poppulate_database import Poppulate

# Homepage route
@app.route('/')
@app.route('/index')
def index():
    Poppulate.poppulate_database()

    recipes = Recipe.query.limit(3).all()
    empty = False
    print(recipes)
    if not recipes:
        empty=True

    return render_template("index.html", recipes=recipes, empty=empty, homepage=True)

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


@app.route('/fetch_recipes/', methods=["GET", "POST"])
@login_required
def fetch_recipes():
    recipes_comprehension = Recipe.query.all()
    # recipes_comprehension = [datetime.date(*[int(y) for y in x.split("-")]) for x in recipes]
    # sorted_recipes = sorted(recipes_comprehension)
    print(recipes_comprehension)
    return jsonify(new_recipes=[recipe.serialize() for recipe in recipes_comprehension])

@app.route('/add_recipe', methods=["GET", "POST"])
def add_recipe():
    if current_user.is_authenticated:
        form = form_ingredients_and_allergens(RecipeForm())
        if form.validate_on_submit():
            f = form.image.data
            print(form.image.data)
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
                author=current_user,
                calories = form.calories.data,
                carbohydrates = form.carbohydrates.data,
                proteins = form.proteins.data,
                fats = form.fats.data,
                cholesterol = form.cholesterol.data
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
            try:
                db.session.add(recipe)
                db.session.commit()
            except:
                print("There was a DB error while saving Recipe.")
            print("Recipe added")

            nutrition = NutritionFacts(
                calories = form.calories.data,
                carbohydrates = form.carbohydrates.data,
                proteins = form.proteins.data,
                fats = form.fats.data,
                cholesterol = form.cholesterol.data,
            )
            try:
                db.session.add(nutrition)
                db.session.commit()
            except:
                print("There was a DB error while saving NutritionFacts.")
            print("NutritionFacts added")

            flash("Congrats, you have added a recipe!")
            return redirect(url_for('recipes_list'))
        else:
            print("Something has failed")

    else:
        flash("You need to login before you add recipe.")
        return redirect(url_for('login'))
    return render_template("add_recipe.html", title='Add Recipe', form=form)


@app.route('/recipe/edit/<recipe_name>', methods=["GET", "POST"])
def edit_recipe(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first_or_404()
    if current_user.is_authenticated and current_user == recipe.author:
        form = form_ingredients_and_allergens(RecipeForm(obj=recipe))
        if form.validate_on_submit():
            f = form.image.data
            filename = secure_filename(f.filename)
            file_path = os.path.join(
                "app/static/img/recipes_images",  filename)
            f.save(file_path)

            created_recipe = Recipe(
                name = form.name.data,
                content = form.content.data,
                cuisine = form.cuisine.data,
                category = form.category.data,
                time_to_prepare = form.time_to_prepare.data,
                serves_num_people = form.serves_num_people.data,
                cooking_time = form.cooking_time.data,
                image = "static/img/recipes_images/" + filename,
                author = current_user,
                calories = form.calories.data,
                carbohydrates = form.carbohydrates.data,
                proteins = form.proteins.data,
                fats = form.fats.data,
                cholesterol = form.cholesterol.data
            )

            ingredients_in_recipe = []
            for ingredient in form.ingredients.data:
                queried_ingredient = Ingredient.query.filter_by(
                    id=ingredient).first()
                ingredients_in_recipe.append(queried_ingredient)
            created_recipe._ingredients = ingredients_in_recipe

            allergens_in_recipe = []
            for allergen in form.allergens.data:
                queried_allergen = Allergen.query.filter_by(
                    id=allergen).first()
                allergens_in_recipe.append(queried_allergen)
            created_recipe._allergens = allergens_in_recipe
            try:
                db.session.delete(recipe)
                db.session.commit()

                db.session.add(created_recipe)
                db.session.commit()
            except:
                print("There was an error while saving changes.")
            flash("Congrats, you have edited a recipe!")
            return redirect(url_for('recipes_list'))
    else:
        flash("You need to login before you edit recipe.")
        return redirect(url_for('login'))
    return render_template("edit_recipe.html", title='Edit Recipe', form=form, recipe=recipe)


@app.route('/delete_recipe/<recipe_name>')
def delete_recipe(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first_or_404()
    db.session.delete(recipe)
    try:
        db.session.delete(recipe)
        db.session.commit()
    except:
        print("There was an error while deleting recipe.")
        flash("There was an error while deleting recipe.")
        return redirect(url_for('index'))
    flash("Your recipe has been deleted.")
    return redirect(url_for('recipes_list'))

@app.route('/recipe/<recipe_name>')
def recipe(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first_or_404()
    content = re.split(r' *[\.\?!][\'"\)\]]* *', recipe.content)
    short_summary = content[0]
    return render_template("recipe_page.html", recipe=recipe, content=content, short_summary=short_summary, nutrition_facts=render_template("_nutrition_facts.html", recipe=recipe))


@app.route('/recipes_list', methods=["GET", "POST"])
def recipes_list():
    form = form_ingredients_and_allergens(SearchForm())
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.paginate(page, 3, False)
    empty = False
    print(recipes)
    if not recipes.items:
        print("Somethin")
        empty = True

    next_url = url_for('recipes_list', page=recipes.next_num) if recipes.has_next else None
    prev_url = url_for('recipes_list', page=recipes.prev_num) if recipes.has_prev else None
    form.any_ingredients.choices = ["All of selected ingredients", "Any of selected ingredients"]

    return render_template("recipes_list.html", title='Recipes', form=form, recipes=recipes.items,
        next_url=next_url, prev_url=prev_url, empty=empty)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    return render_template("contact.html", form=form, )


@app.route('/search_handler', methods=["POST"])
def search_handler():
    category_form = request.form.get('category')
    ingredients_form = request.form.getlist('ingredients[]')
    allergens_form = request.form.getlist('allergens[]')
    choose_ingredients = request.form.get('choose_ingredients')
    sort_by = request.form.get('sort_by')
    print(sort_by)
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
            recipes_with_allergens = []
            for allergen in allergens_form:
                recipes_with_allergens.extend(Recipe.query.filter(
                    Recipe._allergens.any(Allergen.id == allergen)).all())
            print(recipes_with_allergens)
            print(allergens_form)
            print(queried_recipes)
            queried_recipes = set(queried_recipes) - \
                set(recipes_with_allergens)
            print(queried_recipes)

    queried_recipes = list(set(queried_recipes))
    form = SearchForm()
    ingredients = Ingredient.query.all()
    categories = Category.query.all()
    cuisines = Cuisine.query.all()
    first_three_ingredients = Ingredient.query.limit(3).all()
    allergens = Allergen.query.all()
    return render_template("recipes_list.html", form=form, recipes=queried_recipes, categories=categories, cuisines=cuisines,
                           ingredients=ingredients, first_three_ingredients=first_three_ingredients, allergens=allergens)

def form_ingredients_and_allergens(form):
    form.ingredients.choices = db.session.query(
        Ingredient.id, Ingredient.name).all()
    form.allergens.choices = db.session.query(
        Allergen.id, Allergen.name).all()
    return form