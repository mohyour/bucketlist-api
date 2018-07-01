import os
import unittest
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src import db, create_app
from src.models import User, BucketList


app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def seed_db():
    """Seeds the database."""
    password = os.getenv('PASSWORD')
    email = os.getenv('EMAIL')
    bucket = os.getenv('BUCKETLIST')
    user = User(email=email, password=password)
    user.save()
    bucketlist = BucketList(name=bucket, owner=user.id)
    bucketlist.save()


if __name__ == "__main__":
    manager.run()
