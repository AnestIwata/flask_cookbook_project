from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Association tables for recipe search.
ingredients_in_recipe = db.Table(
    '_ingredients',
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)

allergens_in_recipe = db.Table(
    '_allergens',
    db.Column('allergen_id', db.Integer, db.ForeignKey('allergen.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    recipes = db.relationship('Recipe', backref='author', lazy='dynamic')
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisine.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    serves_num_people = db.Column(db.Integer)
    time_to_prepare = db.Column(db.Integer)
    cooking_time = db.Column(db.Integer)
    image = db.Column(db.String(64))

    # Many to many relations
    _ingredients = db.relationship(
        "Ingredient",
        secondary=ingredients_in_recipe,
        back_populates="recipes")

    _allergens = db.relationship(
        "Allergen",
        secondary=allergens_in_recipe,
        back_populates="recipes")

    def __repr__(self):
        return '<Recipe {}>'.format(self.name)


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    recipes = db.relationship(
        "Recipe",
        secondary=ingredients_in_recipe,
        back_populates="_ingredients")

    def __repr__(self):
        return '<Ingredient {}>'.format(self.name)


class Allergen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    recipes = db.relationship(
        "Recipe",
        secondary=allergens_in_recipe,
        back_populates="_allergens")

    def __repr__(self):
        return '<Allergen {}>'.format(self.name)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    recipes = db.relationship('Recipe', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    def get_all_categories():
        return Category.query


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    users = db.relationship('User', backref='country', lazy='dynamic')

    def __repr__(self):
        return '<Country {}>'.format(self.name)

    def get_all_countries():
        return Country.query


class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    recipes = db.relationship('Recipe', backref='cuisine', lazy='dynamic')

    def __repr__(self):
        return '<Cuisine {}>'.format(self.name)

    def get_all_cuisines():
        return Cuisine.query
