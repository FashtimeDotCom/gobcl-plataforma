# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 15:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0005_auto_20171201_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='image',
            field=filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.FILER_IMAGE_MODEL, verbose_name='image'),
        ),
    ]
