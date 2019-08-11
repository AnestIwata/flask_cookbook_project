from app import app, db
from app.models import User, Recipe, Cuisine, Country, Ingredient

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Recipe': Recipe, 'Cuisine': Cuisine, 'Country': Country, 'Ingredient': Ingredient}