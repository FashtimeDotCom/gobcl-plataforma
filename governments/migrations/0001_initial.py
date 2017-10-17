# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Government',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='edition date', null=True)),
                ('publication_date', models.DateField(verbose_name='publication date')),
                ('current_government', models.BooleanField(default=False, verbose_name='current government')),
            ],
            options={
                'verbose_name': 'government',
                'verbose_name_plural': 'governments',
                'permissions': (('view_government', 'Can view governments'),),
            },
        ),
    ]
