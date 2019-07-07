from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from app import app

# Homepage route
@app.route('/')
@app.route('/index')
def home_page():
    return render_template("index.html")

# Login page route
@app.route('/login')
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
