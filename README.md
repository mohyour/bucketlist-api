# Bucket List API

A bucket list is a list of things you intend to achieve or experience.

### Technologies
- Python3
- Flask
- Flask-API
- SQLAlchemy
- autoenv

### Setup
- Create a virtual environent using python3 and activate it
- create a `.env` to have your app configurations like this

      export FLASK_APP="manage.py"
      export SECRET="<your secret>"
      export APP_SETTINGS="development"
      export DATABASE_URL="postgres://localhost/<database-name>"

Activate your .env file by typing `source .env` in the commandline

- Install requirements.txt `pip install -r requirements.txt`
- Ensure your postgres is running on the right port(5432 by default). Create test and development database using `createdb database-name`

### Database
- Run `python manage.py db init` to create a migrations folder
- Run `python manage.py db migrate` to create migrations
- Run `python manage.py db upgrade` to apply the migrations to database

You can seed data into the database by running `python manage.py seed_db`. Ensure the required data has been included in the .env file as follows

      export USERNAME="<your-username>"
      export PASSWORD="<your-password>"
      export EMAIL="your-email"
      export BUCKETLIST="<your-bucketlist>"

Type `source .env` in the commandline to activate

### Starting application
- Run app with `flask run` or `python manage.py runserver`
- Navigate to `http://localhost:5000/` or `http://127.0.0.1:5000/` to use api

### Testing
- Run tests with `python manage.py test`. This makes use of the testing environment 

### API Endpoints
Bucketlist:

| Endpoints	| Methods	|Description|
| ------------- | ------------- | -----|
|/auth/signup | POST | Create a new user |
|/auth/signin | POST | Sign in a user |
|/lists/	|GET	| Get all bucketlists|
|/lists/	|POST	| Add bucketlist |
|/lists/:id	|GET	| Get a single bucketlist |
|/lists/:id	|PUT	| Update a single bucketlist |
|/lists/:id	|DELETE| Delete a single bucketlist |
