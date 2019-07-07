from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from app import app
from app.forms import LoginForm, RecipeForm

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
    return render_template("addRecipe.html", title='Add Recipe', form=form)

if __name__ == "__main__":
    app.run(debug=True)

