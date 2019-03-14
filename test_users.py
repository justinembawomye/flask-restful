import unittest
from resources import *
from . models import UserModel
from run import app, api
import json



    def test_register_user(unittest.TestCase):
        """Test user registers successfully"""
        response = self.test_client.post(
            '/registration', data=json.dumps({"username":"Justine", "password":"123"}), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("User Justine has been registered", str(response.data))

