# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-21 11:49
from __future__ import unicode_literals

from django.db import migrations
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('public_servants', '0010_auto_20171221_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicservanttranslation',
            name='description',
            field=djangocms_text_ckeditor.fields.HTMLField(verbose_name='description'),
        ),
    ]
