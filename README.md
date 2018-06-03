# Bucket List API

A bucket list is a list of things you intend to achieve or experience.

### Technologies
- Python3
- Flask
- Flask-api
- PostgresSQL

### Setup
- Create a virtual environent using python3 and activate it
- create a `.env` to have your app configurations like this

      export FLASK_APP="app.py"
      export SECRET="<your secret>"
      export APP_SETTINGS="development"
      export DATABASE_URL="postgres://localhost/<database-name>"

- Install requirements.txt `pip install -r requirements.text`
- Ensure your postgres is running on the right port(5432 by default). Create test and development database using `createdb database-name`
