""" this document defines the users app urls """
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from users import views as users_views

urlpatterns = [
    url(
        r'^login/$',
        users_views.LoginView.as_view(),
        name='login'
    ),
    url(
        r'^password-change/$',
        users_views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    url(
        r'^password_change/done/$',
        users_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
    url(
        r'^logout/$',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    url(
        r'^password-reset/$',
        users_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        users_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    url(
        r'^verify/(?P<uidb36>[0-9A-Za-z]{1,13})-'
        '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        users_views.user_new_confirm,
        name='user_new_confirm'
    ),
    url(
        r'^reset/done/$',
        users_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    url(
        r'^password-reset/done/$',
        users_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    url(
        r'^edit/$',
        users_views.user_edit,
        name='user_edit'
    ),
    url(
        r'^profile/$',
        users_views.user_profile,
        name='user_profile'
    ),
    url(
        r'^font-size-change/$',
        users_views.user_font_size_change,
        name='user_font_size_change'
    ),
    url(
        r'^clave-unica/login/$',
        users_views.clave_unica_login,
        name='clave_unica_login'
    ),
]


callback_pattern = [
    url(
        r'^$',
        users_views.clave_unica_callback,
        name='clave_unica_callback',
    ),
]
