import os, re, json, sqlalchemy
from collections import Counter
from datetime import datetime 
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug import secure_filename
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RecipeForm, ContactForm, RegistrationForm, SearchForm, CommentForm
from app.models import Recipe, User, Ingredient, Country, Category, Allergen, Cuisine, Comment
from app.poppulate_database import Poppulate

# Homepage route
@app.route('/')
@app.route('/index')
def index():
    Poppulate.poppulate_database()

    recipes = Recipe.query.limit(3).all()
    empty = False
    if not recipes:
        empty=True
    return render_template("index.html", recipes=recipes, empty=empty, sortkey='timestamp', reverse=True)

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

        recipes = Recipe.query.limit(3).all()
        empty = False
        if not recipes:
            empty=True
        return render_template('index.html', title='Homepage', empty=empty, sortkey='timestamp', reverse=True)
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
    return jsonify(new_recipes=[recipe.serialize() for recipe in recipes_comprehension])

@app.route('/add_recipe', methods=["GET", "POST"])
def add_recipe():
    if current_user.is_authenticated:
        form = form_ingredients_and_allergens(RecipeForm(original_name=""))
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

            flash("Congrats, you have added a recipe!") 
            return redirect(url_for('recipe', recipe_name=form.name.data))
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
        form = form_ingredients_and_allergens(RecipeForm(obj=recipe, original_name=recipe.name))
        if form.validate_on_submit() and form.validate_recipe_name:
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
                db.session.query(Recipe).filter(Recipe.id==recipe.id).delete()
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

@app.route('/recipe/<recipe_name>',methods=['GET','POST'])
def recipe(recipe_name):
    recipe = Recipe.query.filter_by(name=recipe_name).first_or_404()
    userIsAnAuthor = False
    comment_form = CommentForm()
    comments = Comment.query.filter_by(recipe_id=recipe.id).all()
    if current_user.is_authenticated and current_user == recipe.author:
        userIsAnAuthor = True

    content = re.split(r' *[\.\?!][\'"\)\]]* *', recipe.content)
    short_summary = content[0]

    if comment_form.validate_on_submit():
        created_comment = Comment(
            name = comment_form.name.data,
            email = comment_form.email.data,
            website = comment_form.website.data,
            comment = comment_form.comment.data,
            recipe_id= recipe.id
        )
        try:
            db.session.add(created_comment)
            db.session.commit()
            redirect(url_for("recipe", recipe_name=recipe.name))
            print("Comment was successfuly added")
        except:
            print("There was a DB error while saving Comment.")
        
    else:
        print("There was an error")
    return render_template("recipe_page.html", recipe=recipe, content=content, short_summary=short_summary, userIsAnAuthor=userIsAnAuthor,
    upvotes=recipe.upvotes, comments=comments, comment_form=comment_form, nutrition_facts=render_template("_nutrition_facts.html", recipe=recipe))


@app.route('/upvote', methods=['POST'])
def upvote():
    if request.method == "POST":
        data_received = json.loads(request.data) 
        recipe = Recipe.query.filter_by(name=data_received['recipe_name']).first()
        if recipe:
            recipe.upvotes += 1
            db.session.commit()
            return json.dumps({'upvotes' : str(recipe.upvotes)})
        return json.dumps({'status' : 'no recipe found'})
    return redirect(url_for('index'))
    
@app.route('/recipes_list', methods=["GET", "POST"])
def recipes_list():
    form = form_ingredients_and_allergens(SearchForm())
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.order_by(Recipe.timestamp.desc()).paginate(page, 9, False)
    empty = False
    if not recipes.items:
        empty = True

    next_url = url_for('recipes_list', page=recipes.next_num) if recipes.has_next else None
    prev_url = url_for('recipes_list', page=recipes.prev_num) if recipes.has_prev else None

    return render_template("recipes_list.html", title='Recipes', form=form, recipes=recipes.items,
        next_url=next_url, prev_url=prev_url, empty=empty)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    return render_template("contact.html", form=form, )

@app.route('/recipes_stats', methods=["GET"]) 
def recipes_stats():
    recipes = Recipe.query.limit(10).all()
    recipe_ids = [recipe.category_id for recipe in recipes]
    recipe_names = [recipe.name for recipe in recipes]
    recipes_upvotes = [recipe.upvotes for recipe in recipes]
    data = Category.query.filter(Category.id.in_(recipe_ids)).all()
    counted_ids = dict(Counter(recipe_ids))
    categories = [category.name for category in data ]
    return render_template("recipes_stats.html", categories=json.dumps(categories), count=json.dumps(list(counted_ids.values())), recipes=json.dumps(recipe_names), upvotes=json.dumps(recipes_upvotes))

@app.route('/search_handler', methods=["POST", "GET"])
def search_handler():
    category_id = request.form.get('category')
    cuisine_id = request.form.get('cuisine')
    ingredients_ids = request.form.getlist('ingredients')
    allergens_ids = request.form.getlist('allergens')
    any_ingredients = request.form.get('any_ingredients')
    sortkey = request.form.get('sortkey')
    form = form_ingredients_and_allergens(SearchForm())
    page = request.args.get('page', 1, type=int)

    search_result = []
    def custom_filter_statement(category_id, cuisine_id):
        if category_id == "1" and cuisine_id == "1":
            return sqlalchemy.sql.true()
        elif cuisine_id == "1":
            return Recipe.category_id == category_id
        elif category_id == "1":
            return Recipe.cuisine_id == cuisine_id
        return sqlalchemy.and_(Recipe.category_id==category_id, Recipe.cuisine_id==cuisine_id)

    def order_recipe_by(sortkey):
        if sortkey=="newest":
            return Recipe.timestamp.desc()
        elif sortkey=="oldest":
            return Recipe.timestamp.asc()
        elif sortkey=="popularity":
            return Recipe.upvotes.desc()
        elif sortkey=="name":
            return Recipe.name
        else:
            return Recipe.timestamp.asc()

    if ingredients_ids and any_ingredients in ["1", "2"]:
        search_result = Recipe.query.filter(
            Recipe._ingredients.any(Ingredient.id.in_(ingredients_ids)),
            ~Recipe._allergens.any(Allergen.id.in_(allergens_ids)),
            custom_filter_statement(category_id, cuisine_id)
            ).order_by(Recipe.timestamp
            ).paginate(page, 9, False)
    else:
        search_result = Recipe.query.filter(
            ~Recipe._allergens.any(Allergen.id.in_(allergens_ids)),
            custom_filter_statement(category_id, cuisine_id)
        ).order_by(order_recipe_by(sortkey)
        ).paginate(page, 9, False)
        
    reverse = False if sortkey == 'name' else True

    next_url = url_for('recipes_list', page=search_result.next_num) if search_result.has_next else None
    prev_url = url_for('recipes_list', page=search_result.prev_num) if search_result.has_prev else None
    
    return render_template("recipes_list.html", title='Recipes', form=form, recipes=search_result.items,
        next_url=next_url, prev_url=prev_url)

def form_ingredients_and_allergens(form):
    form.ingredients.choices = db.session.query(
        Ingredient.id, Ingredient.name).all()
    form.allergens.choices = db.session.query(
        Allergen.id, Allergen.name).all()
    if(isinstance(form, SearchForm)):
        form.sortkey.choices = [('newest', 'Newest'), ('oldest', 'Oldest'), ('popularity', 'Popularity'), ('name', 'Name')]
        form.any_ingredients.choices = [(1, "All of selected ingredients"), (2, "Any of selected ingredients")]

    return form