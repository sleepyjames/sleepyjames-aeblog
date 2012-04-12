from google.appengine.ext import db
from google.appengine.ext import blobstore 

from utils import hash_password

class User(db.Model):
    """ Very basic copy of contrib.auth.models.User
        to allow us to use the basic Django authentication/user
        pattern 
    """

    first_name = db.StringProperty()

    last_name = db.StringProperty()

    username = db.StringProperty()

    email = db.EmailProperty()

    password = db.StringProperty()

    def prepare(self):
        pass

    @property
    def id(self):
        """ We use this to emulate contrib.auth's User models
            id property. Required for login/logout
        """
        return self.key().id()

    def set_password(self, val):
        """ Updates the password hash on the entity  
        """
        self.password = hash_password(val)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def get_full_name(self):
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name, self.last_name)
        else:
            return ''

    @property
    def name_display(self):
        n = self.get_full_name() 
        return n and n or self.username

