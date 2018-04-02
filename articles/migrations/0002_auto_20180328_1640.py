# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-28 19:40
from __future__ import unicode_literals

import cms.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articletranslation',
            name='content',
        ),
        migrations.AddField(
            model_name='article',
            name='content',
            field=cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', slotname='article content', to='cms.Placeholder'),
        ),
        migrations.AlterField(
            model_name='article',
            name='publishing_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='The date this article was published', verbose_name='publishing_date'),
        ),
        migrations.AlterField(
            model_name='articletranslation',
            name='description',
            field=djangocms_text_ckeditor.fields.HTMLField(verbose_name='description'),
        ),
    ]
