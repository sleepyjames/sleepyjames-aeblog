import logging 
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404
from django.views.generic.base import TemplateView 
from django.views.generic.edit import FormView 
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.defaultfilters import date as datefilter

from models import Post
from forms import PostForm 

from core.pagination import Paginator, InvalidPageException


PAGE_SIZE = getattr(settings, 'DEFAULT_PAGE_SIZE', 3)


class PostList(TemplateView):

    template_name = "blog/post_list.html"

    def get_context_data(self, *args, **kwargs):

        ctx = super(PostList, self).get_context_data(*args, **kwargs)

        page = self.request.GET.get('p', 1)

        if self.request.user.is_authenticated():
            objects = Post.all().order("-post_date")
        else:
            objects = Post.published().order("-post_date")


        pager = Paginator(objects, PAGE_SIZE)

        try:
            page_obj = pager.page(page)
        except InvalidPageException:
            raise Http404

        ctx.update({
            'paginator': pager,
            'page_obj': page_obj,
        })

        return ctx


class PostArchiveIndex(TemplateView):

    template_name = "blog/post_archive_index.html"

    def get_context_data(self, *args, **kwargs):

        ctx = super(PostArchiveIndex, self).get_context_data(**kwargs)

        first = Post.all().order("post_date").get()
        latest =  Post.all().order("-post_date").get()
        years = []

        if self.request.user.is_authenticated():
            gql = 'WHERE post_date >= :1 AND post_date < :2'
        else:
            gql = 'WHERE is_published = 1 AND post_date >= :1 AND post_date < :2'

        if latest:

            y = first.post_date.year
            years.append(y)

            y += 1

            while y < latest.post_date.year:

                lower = date(y, 1, 1)
                upper = date(y+1, 1, 1)

                if Post.gql(gql, lower, upper).count() > 0:
                    years.append(y)
                y += 1

            if first.post_date.year != latest.post_date.year:
                years.append(latest.post_date.year)

            years.reverse() 
            ctx['years'] = years

        return ctx


class PostArchive(TemplateView):
    """ Display a list of posts by day/month/year
    """

    template_name = "blog/post_archive.html"

    def get_context_data(self, *args, **kwargs):

        ctx = super(PostArchive, self).get_context_data(*args, **kwargs)

        page = self.request.GET.get('p', 1)
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)
        msg = ""

        try:
            if day and month and year:
                lower_limit = date(int(year), int(month), int(day))
                upper_limit = lower_limit + relativedelta(days=+1)
                msg = "%s" % datefilter(lower_limit, "jS M Y")
            elif month and year:
                lower_limit = date(int(year), int(month), 1)
                upper_limit = lower_limit + relativedelta(months=+1)
                msg = "%s" % datefilter(lower_limit, "F Y")
            elif year:
                lower_limit = date(int(year), 1, 1)
                upper_limit = lower_limit + relativedelta(years=+1)
                msg = "%s" % year
        except ValueError:
            raise Http404

        if self.request.user.is_authenticated():
            gql = "WHERE post_date >= :1 AND post_date <= :2 ORDER BY post_date DESC"
        else:
            gql = "WHERE is_published = 1 AND post_date >= :1 AND post_date <= :2 ORDER BY post_date DESC"

        objects = Post.gql(gql, lower_limit, upper_limit)

        pager = Paginator(objects, PAGE_SIZE)
        page_obj = pager.page(page)

        ctx.update({
            'display_message': msg,
            'paginator': pager,
            'page_obj': page_obj,
            'year': year,
            'month': month,
            'day': day
        })

        return ctx


class PostDetail(TemplateView):

    template_name = "blog/post_detail.html"

    def get_object(self):
        slug = self.kwargs.get('slug', '')

        if self.request.user.is_authenticated():
            qs = Post.all()
        else:
            qs = Post.published()

        try:
            self.object = qs.filter('slug =', slug).fetch(1)[0]
        except IndexError:
            self.object = None

    def get_context_data(self, **kwargs):
        ctx = super(PostDetail, self).get_context_data(**kwargs)
        self.get_object()
        if self.object is None:
            raise Http404
        ctx['object'] = self.object
        return ctx


class BasePostView(FormView):

    template_name = "blog/post_form.html"
    form_class = PostForm

    def form_invalid(self, form):
        messages.error(self.request, u"Sorry there was a problem saving your post. Please check for errors below.")
        return super(BasePostView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('post_edit', args=[self.object.id])


class PostCreate(BasePostView):
    """ Create new post
    """

    def form_valid(self, form):
        data = form.cleaned_data
        data['author'] = self.request.user
        self.object = Post(**data)
        self.object.prepare()
        self.object.put()
        messages.success(self.request, u"Your post was created successfully")
        return super(PostCreate, self).form_valid(form)


class PostEdit(BasePostView):
    """ Edit Post
    """

    def get_object(self):
        pk = self.kwargs.get('pk', 0)
        self.object = Post.get_by_id(int(pk))
        return self.object

    def get_context_data(self, **kwargs):
        ctx = super(PostEdit, self).get_context_data(**kwargs)
        ctx['object'] = self.get_object()
        return ctx

    def get_initial(self):
        self.get_object()
        if not self.object:
            raise Http404
        return {
            'title': self.object.title,
            'is_published': self.object.is_published,
            'content': self.object.content,
            'post_date': self.object.post_date
        }

    def form_valid(self, form):
        data = form.cleaned_data
        self.object.title = data['title']
        self.object.content = data['content']
        self.object.post_date = data['post_date']
        self.object.is_published = data['is_published']
        self.object.prepare()
        self.object.put()
        messages.success(self.request, u"Your post was updated successfully")
        return super(PostEdit, self).form_valid(form)


class PostDelete(TemplateView):

    template_name = "blog/post_delete.html"

    def get_object(self):
        id = self.kwargs.get('pk', '')
        self.object = Post.get_by_id(int(id))

    def get_context_data(self, *args, **kwargs):
        ctx = super(PostDelete, self).get_context_data(**kwargs)
        self.get_object()
        ctx['object'] = self.object
        return ctx

    def post(self, *args, **kwargs):

        self.get_object()
        if not self.object:
            raise Http404
        title = self.object.title
        self.object.delete()
        messages.success(self.request, u"Your post '%s' was deleted successfully" % title)

        return redirect('/')

