import logging
import math

class InvalidPageException(Exception):
    pass

class Paginator:

    def __init__(self, objects, per_page=10, page=1):
        self.objects = objects
        self.number = page
        self.per_page = int(per_page)
        self.total = objects.count()

        if self.total > per_page:
            pages = math.ceil(float(self.total) / self.per_page)
            self.page_range = range(1, int(pages) + 1)
        else:
            self.page_range = []

        self.total_pages = len(self.page_range)
        self.is_pageinated = self.total_pages > 1

    def page(self, p):

        p = int(p)

        if p > 1 and p > self.total_pages:
            raise InvalidPageException(u"Page '%s' not in range %s" % (p, self.total_pages))

        # 0 1 2 3 4 5 6 7 9 10 

        # 0 1 2 
        # 3 4 5
        # 6 7 8 

        # offset = p > 1 and ((self.per_page) * (p - 1) - 1) or 0

        if p > 1:
            offset = self.per_page * (p-1) 
        else:
            offset = 0

        logging.debug('Offset limt ---> %s %s' % (offset, self.per_page)) 

        return {
            'paginator': self,
            'has_next_page': p < len(self.page_range),
            'has_prev_page': p > 1,
            'prev_page': p - 1,
            'next_page': p + 1,
            'number': p,
            'object_list': self.objects.fetch(offset=offset, limit=self.per_page)
        }

