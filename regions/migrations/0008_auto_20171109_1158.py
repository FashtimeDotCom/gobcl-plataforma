# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 14:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0007_auto_20171107_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commune',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='commune',
            name='description_es',
        ),
        migrations.RemoveField(
            model_name='commune',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='commune',
            name='name_es',
        ),
    ]
