from django.conf import urls
from django.contrib.auth import views as auth_views
from django.core import urlresolvers
from django.utils import functional as functional_utils
from django.views import generic

from . import decorators, forms, views

# We pass redirect targets as a lazy unicode string as we are backreferencing.
# We wrap views with custom decorators to force anonymous and authenticated access to them (it is strange to
# try to register a new account while still logged in with another account). We redirect the user away and tell
# the user what has happened with messages.
# Some views use those decorators already so they are not used here. `logout_redirect` does not require
# authenticated access on purpose.
# We use custom login and logout views which give messages to the user explaining what has happened with login
# and logout. We do not assume the user understands what is happening behind the scenes.
urlpatterns = urls.patterns(
    '',

    urls.url(r'^activate/complete/$', decorators.anonymous_required(function=generic.TemplateView.as_view(template_name='registration/activation_complete.html')), name='registration_activation_complete'),
    urls.url(
        r'^activate/(?P<activation_key>[A-Za-z0-9-_:]+)/$',
        decorators.anonymous_required(function=views.ActivationView.as_view()),
        name='registration_activate'
    ),
    urls.url(
        r'^register/$',
        decorators.anonymous_required(function=views.RegistrationView.as_view()),
        name='registration_register'
    ),
    urls.url(r'^register/complete/$', decorators.anonymous_required(function=generic.TemplateView.as_view(template_name='registration/registration_complete.html')), name='registration_complete'),
    urls.url(r'^register/closed/$', decorators.anonymous_required(function=generic.TemplateView.as_view(template_name='registration/registration_closed.html')), name='registration_disallowed'),
    urls.url(r'^email/change/complete/$', decorators.anonymous_required(function=generic.TemplateView.as_view(template_name='registration/email_change_complete.html')), name='email_change_complete'),
    urls.url(r'^login/$', 'nodewatcher.extra.accounts.views.login', name='auth_login'),
    urls.url(r'^logout/$', 'nodewatcher.extra.accounts.views.logout_redirect', name='auth_logout'),
    urls.url(r'^password/change/$', decorators.authenticated_required(function=auth_views.password_change), {
        'post_change_redirect': functional_utils.lazy(urlresolvers.reverse, str)('AccountsComponent:auth_password_change_done'),
        'password_change_form': forms.PasswordChangeForm,
    }, name='auth_password_change'),
    urls.url(r'^password/change/complete/$', decorators.authenticated_required(function=auth_views.password_change_done), name='auth_password_change_done'),
    urls.url(r'^password/reset/$', decorators.anonymous_required(function=auth_views.password_reset), {
        'email_template_name': 'registration/password_reset_email.txt',
        'password_reset_form': forms.PasswordResetForm,
        'post_reset_redirect': functional_utils.lazy(urlresolvers.reverse, str)('AccountsComponent:auth_password_reset_done'),
    }, name='auth_password_reset'),
    urls.url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', decorators.anonymous_required(function=auth_views.password_reset_confirm), {
        'set_password_form': forms.SetPasswordForm,
        'post_reset_redirect': functional_utils.lazy(urlresolvers.reverse, str)('AccountsComponent:auth_password_reset_complete'),
    }, name='auth_password_reset_confirm'),
    urls.url(r'^password/reset/complete/$', decorators.anonymous_required(function=auth_views.password_reset_complete), name='auth_password_reset_complete'),
    urls.url(r'^password/reset/done/$', decorators.anonymous_required(function=auth_views.password_reset_done), name='auth_password_reset_done'),
    urls.url(r'^$', 'nodewatcher.extra.accounts.views.account', name='user_account'),
)
