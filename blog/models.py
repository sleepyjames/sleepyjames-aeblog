from google.appengine.ext import db

from auth.models import User 

from core.utils import make_slug_for_model


class Category(db.Model):
    """ A Post category
    """
    title = db.StringProperty()
    slug = db.StringProperty()

    def prepare(self):
        make_slug_for_model(self, "title", "slug")

    @property
    def id(self):
        return self.key().id()


class Post(db.Model):
    """ A blog post
    """

    title = db.StringProperty()
    slug = db.StringProperty()
    is_published = db.BooleanProperty()
    content = db.StringProperty(multiline=True)
    post_date = db.DateProperty()
    author = db.ReferenceProperty(User)
    category = db.ReferenceProperty(Category)

    created = db.DateTimeProperty(auto_now_add=1)
    modified = db.DateTimeProperty(auto_now=1)

    def prepare(self):
        make_slug_for_model(self, "title", "slug")

    @property
    def id(self):
        return self.key().id()

    @classmethod
    def published(cls):
        return cls.all().filter('is_published =', True)


