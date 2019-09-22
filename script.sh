rm /Users/rrosa/Documents/personal_projects/flask_cookbook_project/app.db
rm -R /Users/rrosa/Documents/personal_projects/flask_cookbook_project/migrations
flask db init
flask db migrate
flask db upgrade