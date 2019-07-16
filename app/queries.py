from app import db
from app.models import Category 

def categories():
        return db.session.query(Category.name).all()