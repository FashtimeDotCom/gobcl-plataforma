# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 15:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ministries', '0010_auto_20171129_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='MinistryTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('slug', models.SlugField(blank=True, editable=False, max_length=255, verbose_name='slug')),
            ],
            options={
                'db_table': 'ministries_ministry_translation',
                'managed': True,
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'ministry Translation',
            },
        ),
        migrations.RemoveField(
            model_name='publicservice',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='publicservice',
            name='name_es',
        ),
        migrations.AlterUniqueTogether(
            name='ministry',
            unique_together=set([]),
        ),
        migrations.AddField(
            model_name='ministrytranslation',
            name='master',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='ministries.Ministry'),
        ),
        migrations.RemoveField(
            model_name='ministry',
            name='description',
        ),
        migrations.RemoveField(
            model_name='ministry',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='ministry',
            name='description_es',
        ),
        migrations.RemoveField(
            model_name='ministry',
            name='name',
        ),
        migrations.RemoveField(
            model_name='ministry',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='ministry',
            name='name_es',
        ),
        migrations.RemoveField(
            model_name='ministry',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='ministry',
            name='slug_en',
        ),
        migrations.RemoveField(
            model_name='ministry',
            name='slug_es',
        ),
        migrations.AlterUniqueTogether(
            name='ministrytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
