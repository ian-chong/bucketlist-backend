import json
import nose
from flask_testing import TestCase
from app import db
from run import app
from app.models import User, Bucketlist
from config.config import app_config


app.config.from_object(app_config["testing"])


class TestBase(TestCase):
    """ Base configurations for the tests """

    def create_app(self):
        """ Returns app """
        return app

    def setUp(self):
        """ Create test database and set up test client """
        self.app = app.test_client()
        db.create_all()
        user = User(username="testuser", password="testpassword")
        bucketlist1 = Bucketlist(title="Knowledge Goals",
                                 description="Things to learn",
                                 created_by=1)
        bucketlist2 = Bucketlist(title="Adventures",
                                 description="Awesome adventures to go on",
                                 created_by=1)
        db.session.add(user)
        db.session.add(bucketlist1)
        db.session.add(bucketlist2)
        db.session.commit()

    def test_index(self):
        """ Test response to the index route """
        request = self.app.get("/api/v1.0/")
        self.assertEqual(request.status_code, 200)
        output = json.loads(request.data)
        self.assertEqual(output, {"Message": "Welcome to the Bucket List API. "
                                  "Register a new user or login to get "
                                  "started!"})

    def tearDown(self):
        """ Destroy test database """
        db.session.remove()
        db.drop_all()

if __name__ == "__main__":
    nose.run()
