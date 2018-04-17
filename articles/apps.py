# -*- coding: utf-8 -*-
""" AppConfig for the articles application. """

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ArticlesConfig(AppConfig):
    verbose_name = _('articles')
    name = 'articles'
