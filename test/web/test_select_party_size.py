from flask_testing import TestCase
from flask import Flask


class SelectPartySize(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_assert_mytemplate_used(self):
        self.client.get("/select-party-size")
        self.assert_template_used('select-party-size.html')
