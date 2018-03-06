# -*- coding: utf-8 -*-
""" Forms for the institutions application. """
# standard library

# django
from django import forms
from django.utils.translation import ugettext_lazy as _

# models
from aldryn_newsblog.models import Article
from .models import ContentPlugin

# views
from base.forms import BaseModelForm


class NoValidateMultipleChoiceField(forms.MultipleChoiceField):

    '''
    MutipleChoiceField without validating choices
    '''

    def validate(self, value):
        pass


class ArticleForm(forms.Form):

    related = NoValidateMultipleChoiceField(
            _('related')
        )
    
    def __init__(self, *args, **kwargs):
        self.article = kwargs.pop('article') 
        super(ArticleForm, self).__init__(*args, **kwargs)

        # get choices from related news from article object
        related_news = list(
            self.article.related.translated().values_list(
                'pk',
                'translations__title',
            )
        )

        self.fields['related'].choices = related_news
