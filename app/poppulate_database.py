from app.models import Category, Ingredient, Allergen
from app import db

class Poppulate():
    def poppulate_database():
        if (Category.query.all() == []):
            categories = ["All","Breakfast","Lunch","Beverages","Appetizers","Soups","Salads","Beef","Poultry","Pork",
            "Seafood","Vegetarian","Vegetables","Desserts","Canning/Freezing","Breads","Holidays"]

            for category in categories:
                    db_category = Category(name=category)
                    db.session.add(db_category)

            db.session.commit()

        if (Ingredient.query.all() == []):
            ingredients = ["sugar", "wheat-flour", "baking-powder", "eggs", "salt", "brown-sugar", 
            "chicken-breast","garlic","milk","oil","sesame-oil","soy-sauce","butter","carrots","coconut-flakes",
            "honey","mung-bean-sprouts","noodles","onion","potato-starch","red-bell-pepper","walnuts","water","almonds",
            "baking-soda","beef-brisket","beef-sirloin","bell-pepper","broth","carrot","cherries","chocolate","cinnamon",
            "cinnamon-stick","cocoa-powder","coconut","corn-tortillas","dark-chocolate","dried-black-mushrooms","dried-soba",
            "egg","five-spice-powder","flour","ginger","guilin-chili-sauce","leek","lettuce","olive-oil","oyster-sauce","pear-juice",
            "pepper","pineapple","red-onion","redcurrant","ribs-of-celery","sichuan-pepper" ,"spring-onions" ,"strawberries","taiwanese-golden-mushrooms",
            "yeast","yellow-bell-pepper"]
        
            for ingredient in ingredients:
                    db_ingredient = Ingredient(name=ingredient)
                    db.session.add(db_ingredient)
            
            db.session.commit()