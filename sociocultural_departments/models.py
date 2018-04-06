# -*- coding: utf-8 -*-
""" Models for the sociocultural_departments application. """
# standard library

# django
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from djangocms_text_ckeditor.fields import HTMLField
from easy_thumbnails.fields import ThumbnailerImageField

from parler.models import TranslatableModel
from parler.models import TranslatedFields

from base.models import BaseModel
from base.models import file_path
from base.models import lastest_government_structure

from .managers import SocioculturalDepartmentQueryset
from .managers import SocioculturalDepartmentURLQueryset


class SocioculturalDepartmentURL(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(
            _('name'),
            max_length=100,
            null=True,
        ),
        description=HTMLField(
            _('description'),
        ),
    )
    url = models.URLField(
        _('url'),
        max_length=200,
    )
    order = models.PositiveIntegerField(
        _('order'),
        default=0,
    )

    objects = SocioculturalDepartmentURLQueryset.as_manager()

    def __str__(self):
        return self.url

    class Meta:
        ordering = ('order',)
        verbose_name = _('sociocultural department url')
        verbose_name_plural = _('sociocultural department urls')
        permissions = (
            ('view_socioculturaldepartment_url', _(
                'Can view sociocultural department url')),
        )

    def get_absolute_url(self):
        return self.url


class SocioculturalDepartment(BaseModel, TranslatableModel):
    government_structure = models.OneToOneField(
        'government_structures.GovernmentStructure',
        verbose_name=_('government structure'),
        default=lastest_government_structure,
    )
    name = models.CharField(
        _('name'),
        max_length=100,
    )
    translations = TranslatedFields(
        title=models.CharField(
            _('title'),
            max_length=50,
        ),
        description=HTMLField(
            _('description'),
        ),
    )
    photo = ThumbnailerImageField(
        _('photo'),
        upload_to=file_path,
        null=True,
    )
    twitter = models.CharField(
        max_length=50,
    )
    url = models.URLField(
        _('url'),
        max_length=200,
    )
    urls = models.ManyToManyField(
        SocioculturalDepartmentURL,
        verbose_name=_('urls'),
    )

    objects = SocioculturalDepartmentQueryset.as_manager()

    class Meta:
        verbose_name = _('sociocultural department')
        verbose_name_plural = _('sociocultural departments')
        permissions = (
            ('view_socioculturaldepartment', _(
                'Can view sociocultural department')),
        )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sociocultural_department_detail')
