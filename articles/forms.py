# -*- coding: utf-8 -*-
""" Forms for the articles application. """
# standard library

# django

# models
from .models import Article

# parler
from parler.forms import TranslatableModelForm



class ArticleForm(TranslatableModelForm):
    """
    Form Article model.
    """

    class Meta:
        model = Article
        fields = (
            'title',
            'lead_in',
            'featured_image',
            'publishing_date',
        )

    class Media:
        extend = False
        css = {
            'all': [
                'filer/css/admin_filer.css',
            ]
        }
        js = (
            'admin/js/core.js',
            'admin/js/jquery.js',
            'admin/js/jquery.init.js',
            'admin/js/admin/RelatedObjectLookups.js',
            'admin/js/actions.js',
            'admin/js/urlify.js',
            'admin/js/prepopulate.js',
            'filer/js/libs/dropzone.min.js',
            'filer/js/addons/dropzone.init.js',
            'filer/js/addons/popup_handling.js',
            'filer/js/addons/widget.js',
            'admin/js/related-widget-wrapper.js',
        )

    def save(self, commit=True):
        article = super(ArticleForm, self).save(commit=False)
        article.created_by = self.user
        article.save()
        return article
