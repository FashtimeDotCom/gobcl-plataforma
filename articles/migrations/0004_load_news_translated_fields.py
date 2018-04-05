# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-04 17:49
from __future__ import unicode_literals

from django.db import migrations


def load_translations(apps, schema_editor):
    Article = apps.get_model('articles', 'Article')
    OldArticle = apps.get_model('aldryn_newsblog', 'Article')
    ArticleTranslation = apps.get_model('articles', 'ArticleTranslation')

    for old_article in OldArticle.objects.all():
        article = Article.objects.get(content_id=old_article.content_id)

        # copy translations
        for translation in old_article.translations.all():
            ArticleTranslation.objects.create(
                master_id=article.pk,
                language_code=translation.language_code,
                title=translation.title,
                slug=translation.slug,
                lead_in=translation.lead_in,
                meta_title=translation.meta_title,
                meta_description=translation.meta_description,
                meta_keywords=translation.meta_keywords,
                search_data=translation.search_data,
                is_featured=old_article.is_featured,
                is_published=old_article.is_published,
            )


def unload_translations(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20180404_1640'),
    ]

    operations = [
        migrations.RunPython(load_translations, unload_translations),
    ]
