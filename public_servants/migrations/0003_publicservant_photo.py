# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 15:19
from __future__ import unicode_literals

import base.models
from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('public_servants', '0002_publicservant_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicservant',
            name='photo',
            field=easy_thumbnails.fields.ThumbnailerImageField(null=True, upload_to=base.models.file_path, verbose_name='photo'),
        ),
    ]
