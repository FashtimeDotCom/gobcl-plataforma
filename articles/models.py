# -*- coding: utf-8 -*-
""" Models for the articles application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import activate
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel
from cms.models.fields import PlaceholderField
from djangocms_text_ckeditor.fields import HTMLField

from parler.models import TranslatableModel
from parler.models import TranslatedFields
from filer.fields.image import FilerImageField
from cms.utils.i18n import get_current_language

from .managers import ArticleQueryset


class Article(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(
            _('title'),
            max_length=255,
            unique=True,
        ),
        slug=models.SlugField(
            _('slug'),
            max_length=255,
        ),
        description=HTMLField(
            _('description'),
        ),
    )
    image = FilerImageField(
        verbose_name=_('image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='article_image'
    )
    is_featured = models.BooleanField(
        _('is featured'),
        default=False,
    )
    publishing_date = models.DateTimeField(
        _('publishing_date'),
        default=timezone.now,
        help_text=_("The date this article was published"),
    )
    content = PlaceholderField(
        'article content',
        on_delete=models.SET_NULL,
        related_name='articles',
    )

    objects = ArticleQueryset.as_manager()

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = (
            '-publishing_date',
        )
        permissions = (
            ('view_article', _('Can view article')),
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        language = get_current_language()
        activate(language=language)
        self.slug = slugify(self.title)
        return super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article_detail', args=(self.slug,), )
