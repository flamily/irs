from flask_testing import TestCase
from flask import Flask


class SelectPartySize(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_assert_url(self):
        self.client.get("/select-party-size")
