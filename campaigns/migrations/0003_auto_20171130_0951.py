# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 12:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0002_auto_20171127_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='description_en',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='description_es',
            field=models.TextField(null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='title_en',
            field=models.CharField(max_length=100, null=True, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='title_es',
            field=models.CharField(max_length=100, null=True, verbose_name='title'),
        ),
    ]
