import urlparse

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import base36_to_int
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site

from django.views.generic.base import TemplateView 
from django.views.generic.edit import FormView 
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages


from models import User
from forms import UserForm, UserEditForm


def create_user(request):

    try:
        u = User.all().filter("username = ", "admin").fetch(1)[0]
    except IndexError:
        u = None

    if not u:
        u = User(username="admin")
        u.set_password('password')
        u.put()

    return HttpResponse(u"Created")


@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = None # get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        #'site': current_site,
        #'site_name': current_site.name,
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request, current_app=current_app))

def logout(request, next_page=None,
           template_name='registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if redirect_to:
        netloc = urlparse.urlparse(redirect_to)[1]
        # Security check -- don't allow redirection to a different host.
        if not (netloc and netloc != request.get_host()):
            return HttpResponseRedirect(redirect_to)

    if next_page is None:
        current_site = get_current_site(request)
        context = {
            'site': current_site,
            'site_name': current_site.name,
            'title': _('Logged out')
        }
        context.update(extra_context or {})
        return render_to_response(template_name, context,
                                  context_instance=RequestContext(request, current_app=current_app))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)

def logout_then_login(request, login_url=None, current_app=None, extra_context=None):
    """
    Logs out the user if he is logged in. Then redirects to the log-in page.
    """
    if not login_url:
        login_url = settings.LOGIN_URL
    return logout(request, login_url, current_app=current_app, extra_context=extra_context)


class UserList(TemplateView):
    """ List available users
    """

    template_name = "auth/user_list.html"

    def get_context_data(self, *args, **kwargs):

        ctx = super(self.__class__, self).get_context_data(*args, **kwargs)

        ctx.update({
            'object_list': User.all(),
        })

        return ctx


class BaseUserView(FormView):

    template_name = "auth/user_form.html"
    form_class = UserForm

    def form_invalid(self, form):
        messages.error(self.request, u"Sorry there was a problem saving your post. Please check for errors below.")
        return super(BaseUserView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('user_edit', args=[self.object.id])


class UserEdit(BaseUserView):
    """ Edit user 
    """

    form_class = UserEditForm

    def get_object(self):
        pk = self.kwargs.get('pk', 0)
        self.object = User.get_by_id(int(pk))
        return self.object

    def get_context_data(self, **kwargs):
        ctx = super(UserEdit, self).get_context_data(**kwargs)
        ctx['object'] = self.get_object()
        return ctx

    def get_initial(self):
        self.get_object()
        return {
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'username': self.object.username,
        }

    def form_valid(self, form):
        data = form.cleaned_data
        self.object.first_name = data['first_name']
        self.object.last_name = data['last_name']
        self.object.username = data['username']

        # Update password
        new_password = data.get('new_password', '')
        if new_password != '':
            self.object.set_password(new_password)

        self.object.prepare()
        self.object.put()
        messages.success(self.request, u"User was updated successfully")
        return super(UserEdit, self).form_valid(form)

