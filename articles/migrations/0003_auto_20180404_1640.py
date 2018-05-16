# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-04 19:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_load_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=234, verbose_name='title')),
                ('slug', models.SlugField(blank=True, help_text='Used in the URL. If changed, the URL will change. Clear it to have it re-created automatically.', max_length=255, verbose_name='slug')),
                ('lead_in', djangocms_text_ckeditor.fields.HTMLField(blank=True, default='', help_text='The lead gives the reader the main idea of the story, this is useful in overviews, lists or as an introduction to your article.', verbose_name='lead')),
                ('meta_title', models.CharField(blank=True, default='', max_length=255, verbose_name='meta title')),
                ('meta_description', models.TextField(blank=True, default='', verbose_name='meta description')),
                ('meta_keywords', models.TextField(blank=True, default='', verbose_name='meta keywords')),
                ('is_published', models.BooleanField(db_index=True, default=False, verbose_name='is published')),
                ('is_featured', models.BooleanField(db_index=True, default=False, verbose_name='is featured')),
                ('is_dirty', models.BooleanField(default=False, editable=False)),
                ('draft', models.BooleanField(db_index=True, default=True, editable=False)),
                ('search_data', models.TextField(blank=True, editable=False)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='articles.Article')),
            ],
            options={
                'verbose_name': 'article Translation',
                'db_table': 'articles_article_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
        ),
        migrations.AlterUniqueTogether(
            name='articletranslation',
            unique_together=set([('language_code', 'slug', 'draft'), ('language_code', 'master')]),
        ),
    ]
