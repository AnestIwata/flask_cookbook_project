from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from app import app
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

