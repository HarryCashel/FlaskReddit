import unittest
from main import create_app, db
from models.User import User


class TestUsers(unittest.TestCase):
    """A class that creates an instance of our application, creates our database
     and fires some requests to our endpoints"""

    @classmethod
    def setUp(cls):
        """Hook/Fixture to create the app instance and set up the database"""
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db-custom", "seed"])

        print("setup ran")

    @classmethod
    def tearDown(cls):
        """Hook/Fixture to teardown the database"""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

        print("teardown ran")

    def test_user_index(self):
        response = self.client.get("/users/")

        data = response.get_json()
        print(len(data))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_create_user(self):
        response = self.client.post("/users/", json={
            "email": "test1@email.com",
            "username": "testuser",
            "password": "password",
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)


