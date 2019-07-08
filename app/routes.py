from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.forms import LoginForm, RecipeForm
from app.models import Recipe

# Homepage route
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

# Login page route
@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", title='Login', form=form)

@app.route('/add_recipe', methods=["GET", "POST"])
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            name=form.name.data, 
            content=form.content.data, 
            # ingredients=form.ingredients.data,
            # allergens=form.allergens.data,
            cuisine=form.cuisine.data,
            country=form.country.data
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
    recipes = Recipe.query.all()
    return render_template("recipes_list.html", recipes=recipes)
if __name__ == "__main__":
    app.run(debug=True)

