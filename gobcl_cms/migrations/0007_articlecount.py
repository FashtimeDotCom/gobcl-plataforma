# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-08 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gobcl_cms', '0006_headerplugin'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='edition date', null=True)),
                ('visits', models.PositiveIntegerField(default=0, verbose_name='visits')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='count', to='aldryn_newsblog.Article', verbose_name='article')),
            ],
            options={
                'ordering': ('visits',),
            },
        ),
    ]
