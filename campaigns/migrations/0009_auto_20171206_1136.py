# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-06 14:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0008_auto_20171206_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaigntranslation',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='title'),
        ),
    ]
