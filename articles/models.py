# -*- coding: utf-8 -*-
""" Models for the articles application. """
# standard library

# django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import activate
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel
from cms.models.fields import PlaceholderField as OriginalPlaceholderField
from djangocms_text_ckeditor.fields import HTMLField

# external
from sortedm2m.fields import SortedManyToManyField
from .managers import RelatedManager
from taggit.managers import TaggableManager
from aldryn_apphooks_config.fields import AppHookConfigField
from aldryn_categories.fields import CategoryManyToManyField
from cms.exceptions import PublicIsUnmodifiable
from cms.models.pluginmodel import CMSPlugin
from cms.plugin_pool import plugin_pool
from cms.utils.copy_plugins import copy_plugins_to
from cms.utils.i18n import get_current_language
from filer.fields.image import FilerImageField
from parler.models import TranslatableModel
from parler.models import TranslatedFields


class PlaceholderField(OriginalPlaceholderField):
    def pre_save(self, model_instance, add):
        """
        When copying placeholders from aldryn newsblog to this app
        we to need to avoid creating new instances of placehodlers
        """
        if not model_instance.pk and model_instance.content:
            return super(OriginalPlaceholderField, self).pre_save(
                model_instance,
                add
            )

        return super(PlaceholderField, self).pre_save(model_instance, add)


class Article(BaseModel, TranslatableModel):
    update_search_on_save = getattr(
        settings,
        'ALDRYN_NEWSBLOG_UPDATE_SEARCH_DATA_ON_SAVE',
        False
    )

    # foreign keys
    created_by = models.ForeignKey(
        'users.User',
        verbose_name=_('created by'),
        null=True,
        on_delete=models.SET_NULL,
        related_name='articles',
    )
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=234),
        slug=models.SlugField(
            verbose_name=_('slug'),
            max_length=255,
            db_index=True,
            blank=True,
            help_text=_(
                'Used in the URL. If changed, the URL will change. '
                'Clear it to have it re-created automatically.'
            ),
        ),
        lead_in=HTMLField(
            verbose_name=_('lead'), default='',
            help_text=_(
                'The lead gives the reader the main idea of the story, this '
                'is useful in overviews, lists or as an introduction to your '
                'article.'
            ),
            blank=True,
        ),
        meta_title=models.CharField(
            max_length=255,
            verbose_name=_('meta title'),
            blank=True,
            default=''
        ),
        meta_description=models.TextField(
            verbose_name=_('meta description'),
            blank=True,
            default=''
        ),
        meta_keywords=models.TextField(
            verbose_name=_('meta keywords'),
            blank=True,
            default=''
        ),
        is_published=models.BooleanField(
            _('is published'),
            default=False,
            db_index=True
        ),
        is_featured=models.BooleanField(
            _('is featured'),
            default=False,
            db_index=True
        ),
        draft = models.BooleanField(
            default=True,
            editable=False,
            db_index=True,
        ),
        meta={'unique_together': (('language_code', 'slug', 'draft'), )},

        search_data=models.TextField(blank=True, editable=False)
    )
    content = PlaceholderField(
        'article_content',
        on_delete=models.SET_NULL,
        related_name='articles',
    )

    categories = CategoryManyToManyField(
        'aldryn_categories.Category',
        verbose_name=_('categories'),
        blank=True,
        related_name='articles',
    )
    publishing_date = models.DateTimeField(_('publishing date'),
                                           default=timezone.now)
    featured_image = FilerImageField(
        verbose_name=_('featured image'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles',
    )
    tags = TaggableManager(
        blank=True,
        related_name='articles',
    )

    # Setting "symmetrical" to False since it's a bit unexpected that if you
    # set "B relates to A" you immediately have also "A relates to B". It have
    # to be forced to False because by default it's True if rel.to is "self":
    #
    # https://github.com/django/django/blob/1.8.4/django/db/models/fields/related.py#L2144
    #
    # which in the end causes to add reversed releted-to entry as well:
    #
    # https://github.com/django/django/blob/1.8.4/django/db/models/fields/related.py#L977
    related = SortedManyToManyField(
        'self',
        verbose_name=_('related articles'),
        blank=True,
        symmetrical=False
    )
    is_draft = models.BooleanField(
        default=True,
        editable=False,
        db_index=True,
    )

    public = models.OneToOneField(
        'self',
        related_name='draft_article',
        null=True,
        editable=False
    )

    objects = RelatedManager()

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = (
            '-publishing_date',
        )
        permissions = (
            ('view_article', _('Can view article')),
        )

    # private methods
    def __str__(self):
        return self.title

    def _copy_attributes(self, target, language):
        """
        Copy all page data to the target. This excludes parent and other values
        that are specific to an exact instance.
        :param target: The Article to copy the attributes to
        """
        translation = self.translations.get(language_code=language)

        # copy translations
        try:
            new_translation = ArticleTranslation.objects.get(
                master_id=target.pk,
                language_code=language,
            )
        except ArticleTranslation.DoesNotExist:
            ArticleTranslation.objects.create(
                master_id=target.pk,
                language_code=language,
                title=translation.title,
                slug=translation.slug,
                lead_in=translation.lead_in,
                meta_title=translation.meta_title,
                meta_description=translation.meta_description,
                meta_keywords=translation.meta_keywords,
                search_data=translation.search_data,
                draft=False,
                is_published=translation.is_published,
                is_featured=translation.is_featured,
            )
        else:
            new_translation.title = translation.title
            new_translation.draft = False
            new_translation.slug = translation.slug
            new_translation.lead_in = translation.lead_in
            new_translation.meta_title = translation.meta_title
            new_translation.meta_description = translation.meta_description
            new_translation.meta_keywords = translation.meta_keywords
            new_translation.search_data = translation.search_data
            new_translation.is_published = translation.is_published
            new_translation.is_featured = translation.is_featured
            new_translation.save()

        target.featured_image = self.featured_image
        target.publishing_date = self.publishing_date
        target.is_featured = self.is_featured

        target.tags.clear()

        for tag in self.tags.all():
            target.tags.add(tag.name)

    def _copy_contents(self, target, language):
        """
        Copy all the plugins to a new article.
        :param target: The page where the new content should be stored
        """
        # TODO: Make this into a "graceful" copy instead of deleting and overwriting
        # copy the placeholders (and plugins on those placeholders!)

        plugin_pool.set_plugin_meta()
        plugins = CMSPlugin.objects.filter(
            placeholder=self.content,
            language=language
        ).order_by('-depth')

        for plugin in plugins:
            instance, cls = plugin.get_plugin_instance()
            if instance and getattr(instance, 'cmsplugin_ptr_id', False):
                instance.cmsplugin_ptr = plugin
                instance.cmsplugin_ptr._no_reorder = True
                instance.delete(no_mp=True)
            else:
                plugin._no_reorder = True
                plugin.delete(no_mp=True)

        plugins = self.content.get_plugins_list(language)

        # update the page copy
        if plugins:
            copy_plugins_to(plugins, target.content)

    # django methods
    def get_absolute_url(self):
        return reverse('articles:article_detail', args=(self.slug,), )

    # custom methods
    def publish(self, language):
        """
        :returns: the publicated Article.
        """
        # Publish only be called on draft pages
        if not self.is_draft:
            raise PublicIsUnmodifiable(
                'The public instance cannot be published. Use draft.'
            )

        if not self.pk:
            self.save()

        # be sure we have the newest data including tree information
        self.refresh_from_db()

        if self.public_id:
            # Ensure we have up to date mptt properties
            public_article = self.public
        else:
            public_article = Article(created_by=self.created_by)

        if not self.publishing_date:
            self.publishing_date = timezone.now()

        # we need to set relate this new public copy to its draft page (self)
        public_article.public = self
        public_article.is_draft = False

        public_article.save()

        # store the relationship between draft and public
        self.public = public_article
        self.save()

        self._copy_attributes(public_article, language)

        public_article.save()

        # The target page now has a pk, so can be used as a target
        self._copy_contents(public_article, language)

        return public_article
