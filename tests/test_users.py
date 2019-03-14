import unittest
import json

# from resources import app, db
from run import UserRegister, UserLogin


class TestUser(unittest.TestCase):
    """Tests for the user api i.e. user registration, login, logout and password resetting"""

    def create_app(self):
        """Creates the app for testing"""
        app.config.from_object('config.TestingConfig')
        return app
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.session.remove()
        db.drop_all()
        db.create_all()
        self.user = {'user_email' : 'soniak@gmail.com', 'user_name': 'sonjaYXG', 
                    'user_password' : 'qWerty123'}
        self.user_two = {'user_email' : 'karungi@gmail.com', 'user_name': 'Kaynyts000', 
                        'user_password' : 'qWerty123'}

if __name__=='__main__':
    unittest.main()                        


