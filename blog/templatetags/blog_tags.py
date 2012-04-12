from django import template

register = template.Library()

from blog.models import Post


class PostListNode(template.Node):

    def __init__(self, varname, include_draft=True):
        self.varname = varname
        self.include_draft = include_draft

    def render(self, context):

        if self.include_draft:
            qs = Post.all().order('-post_date')
        else:
            qs = Post.published().order('-post_date')

        context[self.varname] = qs

        return ''

@register.tag
def get_published_posts(parser, tokens):
    _tag, _as, varname = tokens.split_contents()
    return PostListNode(varname, include_draft=False)

@register.tag
def get_posts(parser, tokens):
    _tag, _as, varname = tokens.split_contents()
    return PostListNode(varname, include_draft=True)
