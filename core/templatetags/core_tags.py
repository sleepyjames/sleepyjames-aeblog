import logging

from django import template

register = template.Library()

@register.filter
def get_class(object):
    classname = object.__class__.__name__.lower()
    return classname


class PaginationNode(template.Node):
    def __init__(self, object_list, per_page, page, varname):
        self.varname = varname
        self.object_list = template.Variable(object_list)
        self.per_page = per_page
        self.page = page

    def render(self, context):

        object_list = self.object_list.resolve(context)
        pageinator = Paginator(object_list, self.per_page)
        page_obj = paginator.page(self.page)

        context[self.varname] = page_obj

        return ''

@register.tag
def paginate(parser, tokens):
    """ Generate page object for a given object list
            
        Usage: paginate object_list by 10 page 1 as some-var
    """

    _tag, objects, _by, per_page, _get, page, _as, varname = tokens.split_contents()

    return PaginationNode(objects, per_page, page, varname)
