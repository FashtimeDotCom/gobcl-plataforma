# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-29 19:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('government_structures', '0001_initial'),
        ('public_servants', '0005_auto_20171109_1838'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='publicservant',
            unique_together=set([('name', 'government_structure')]),
        ),
    ]
