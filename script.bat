del "C:\Users\Dev\Documents\programowanie\flask_cookbook_project\app.db"
@RD /S /Q "C:\Users\Dev\Documents\programowanie\flask_cookbook_project\migrations"

flask db init
flask db migrate
flask db upgrade