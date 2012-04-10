import logging
from auth.models import User 

from utils import hash_password


class AppEngineEntityAuthBackend:

    def authenticate(self, username=None, password=None):

        if not (username and password):
            return False

        u = User.all()\
            .filter("username =", username)\
            .filter("password =", hash_password(password))
        
        try:
            return u.fetch(1)[0]
        except IndexError:
            return None

    def get_user(self, user_id):
        try:
            return User.get_by_id(user_id)
        except: 
            return None
 
        




