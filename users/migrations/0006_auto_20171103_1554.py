# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-03 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_font_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='font_size',
            field=models.CharField(blank=True, default='default', max_length=100, verbose_name='font size'),
        ),
    ]
