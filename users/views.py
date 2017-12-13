# -*- coding: utf-8 -*-
""" The users app views"""

# standard
import json
import requests
import logging

# django
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.http import base36_to_int
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import CreateView

# forms
from users.forms import AuthenticationForm
from users.forms import CaptchaAuthenticationForm
from users.forms import CaptchaUserCreationForm
from users.forms import UserForm

# models
from users.models import User

# views
from base.views import BaseListView

# utils
from users.login_settings import ClaveUnicaSettings


logger = logging.getLogger('debug_messages')


class LoginView(auth_views.LoginView):
    """ view that renders the login """
    template_name = "registration/login.pug"
    form_class = AuthenticationForm
    title = _('Login')

    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['title'] = self.title

        return context

    def get_form_class(self):
        """
        Returns the form class, if the user has tried too many times to login
        without success, then it passes on the captcha login
        """
        login_try_count = self.request.session.get('login_try_count', 0)

        # If the form has been submitted...
        if self.request.method == "POST":
            self.request.session['login_try_count'] = login_try_count + 1

        if login_try_count >= 20:
            return CaptchaAuthenticationForm

        return super(LoginView, self).get_form_class()


class PasswordChangeView(auth_views.PasswordChangeView):
    """ view that renders the password change form """
    template_name = "registration/password_change_form.pug"


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'registration/password_change_done.pug'


class PasswordResetView(auth_views.PasswordResetView):
    """ view that handles the recover password process """
    template_name = "registration/password_reset_form.pug"
    email_template_name = "emails/password_reset.txt"


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """ view that handles the recover password process """
    template_name = "registration/password_reset_confirm.pug"


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """ View that shows a success message to the user"""
    template_name = "registration/password_reset_done.pug"


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """ View that shows a success message to the user"""
    template_name = "registration/password_reset_complete.pug"


class UserCreateView(CreateView):
    template_name = 'users/create.pug'
    form_class = CaptchaUserCreationForm
    title = _('Registration')

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = self.title

        return context

    def form_valid(self, form):
        form.save(verify_email_address=True, request=self.request)
        messages.add_message(
            self.request,
            messages.INFO,
            _("An email has been sent to you. Please "
              "check it to verify your email.")
        )

        return redirect('home')


@login_required
def user_edit(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Your data has been successfully saved."))
            return redirect('home')
    else:
        form = UserForm(instance=request.user)

    context = {
        'cancel_url': reverse('user_profile'),
        'form': form,
    }

    return render(request, 'users/edit.pug', context)


@login_required
def user_profile(request):
    context = {
        'title': _('My profile')
    }

    return render(request, 'users/detail.pug', context)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def user_new_confirm(request, uidb36=None, token=None,
                     token_generator=default_token_generator,
                     current_app=None, extra_context=None):
    """
    View that checks the hash in a email confirmation link and activates
    the user.
    """

    assert uidb36 is not None and token is not None  # checked by URLconf
    try:
        uid_int = base36_to_int(uidb36)
        user = User.objects.get(id=uid_int)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.update(is_active=True)
        messages.add_message(request, messages.INFO,
                             _("Your email address has been verified."))
    else:
        messages.add_message(request, messages.ERROR,
                             _("Invalid verification link"))

    return redirect('login')


class UserListView(BaseListView):
    model = User
    template_name = 'users/list.pug'
    ordering = ('first_name', 'last_name')

    def get_queryset(self):
        queryset = super().get_queryset()

        # search users
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.search(q)

        queryset = queryset.prefetch_related('groups')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # we want to show a list of groups in each user, so we
        # iterate through each user, and create a string with the groups
        for obj in context['object_list']:
            obj.group_names = ' '.join([g.name for g in obj.groups.all()])

        return context


@csrf_exempt
def user_font_size_change(request):
    """
    Json view that that handles user font size changes
    """

    if request.method == 'POST':
        content = json.loads(request.body.decode('utf-8'))
        request.user.font_size = content['font_size']
        if request.user.is_authenticated:
            request.user.save()
        else:
            request.session['font_size'] = content['font_size']

        return JsonResponse({'font_size': request.user.font_size})

    return JsonResponse({'method error': 'must post'})


def clave_unica_login(request):
    """
    View that redirects to ClaveUnica login site
    with this project's parameters
    """
    clave_unica = ClaveUnicaSettings()
    state = clave_unica.generate_token()
    request.session['state'] = state
    clave_unica_url = clave_unica.get_csrf_redirect_url(state)
    return redirect(clave_unica_url)


def clave_unica_callback(request):
    """
    View that gets or creates a user and logs it in by using
    ClaveUnica's data and athorization
    """

    logger.debug('stifgnig')

    received_state = request.GET.get('state')
    if 'state' not in request.session:
        # TODO: redirect somewhere else or throw a message?
        return redirect('home')

    if received_state != request.session['state']:
        # TODO: redirect somewhere else or throw a message?
        return redirect('home')

    received_code = request.GET.get('code')
    clave_unica = ClaveUnicaSettings()
    data = clave_unica.get_token_url_data(received_state, received_code)
    token_response = requests.post(
        clave_unica.TOKEN_URI,
        data=data,
    )

    if token_response.headers['Content-Type'] == 'text/html':
        pass

    try:
        access_token = token_response.json()['access_token']
        # expires_in = token_response.json['expires_in']
        # id_token = token_response.json['id_token']
        bearer = "Bearer {}".format(access_token)
        headers = {"Authorization": bearer}

        access_response = requests.post(
            ClaveUnicaSettings.USER_INFO_URI,
            headers=headers,
        )

        user = User.clave_unica_get_or_create(access_response)

        logger.debug(user)

        return redirect('home')
    except ValueError:
        # TODO: redirect somewhere else or throw a message?
        return redirect('home')

    return redirect('home')
