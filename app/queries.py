from app import app, db
from app.models import Category 

def categories():
        return Category.query.all()
        # return db.session.query(Category.name).all()