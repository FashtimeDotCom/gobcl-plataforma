# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-09 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('government_structures', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='governmentstructure',
            name='archive_news',
            field=models.BooleanField(default=False, help_text='archive government news', verbose_name='archive news'),
        ),
    ]
