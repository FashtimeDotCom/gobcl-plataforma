import json

from django.conf import settings
from django.utils.translation import activate
from django.contrib.redirects.models import Redirect
from django.contrib.sites.shortcuts import get_current_site

from djangocms_text_ckeditor.models import Text
from djangocms_picture.models import Picture
from gobcl_cms.models import HtmlPlugin

from base.utils import keymap_replace

from aldryn_newsblog.models import Article
from aldryn_newsblog.models import ArticleTranslation
from filer.models.foldermodels import Folder
from filer.models.imagemodels import Image


def create_text_plugin(content, target_placeholder, language, position):
    '''
    Create text plugin by placeholder
    '''

    text = Text(body=content)
    text.position = position
    text.tree_id = None
    text.lft = None
    text.rght = None
    text.level = None
    text.language = language
    text.plugin_type = 'TextPlugin'
    text.placeholder = target_placeholder
    text.save()


def create_picture_plugin(image, target_placeholder, language, position):
    '''
    Create picture image plugin by placeholder
    '''

    # Create Picture plugin
    picture = Picture.objects.create()
    picture.picture = image
    picture.position = position
    picture.tree_id = None
    picture.lft = None
    picture.rght = None
    picture.level = None
    picture.language = language
    picture.plugin_type = 'PicturePlugin'
    picture.placeholder = target_placeholder
    picture.save()


def reorder_by_folder_feature_image_articles():
    articles = Article.objects.all()

    for article in articles:
        if not article.featured_image_id:
            continue

        publishing_date = article.publishing_date
        year = publishing_date.year
        month = publishing_date.month
        day = publishing_date.day

        folder_year = Folder.objects.get_or_create(name=year)[0]

        forlder_month = Folder.objects.get_or_create(
            name=month,
            parent=folder_year,
        )[0]

        folder_day = Folder.objects.get_or_create(
            name=day,
            parent=forlder_month,
        )[0]

        image = article.featured_image

        image.folder = folder_day
        image.save()


def generate_sha1_to_image():

    images = Image.objects.filter(sha1='').order_by('id')
    print(images.count())

    while images.exists():
        for image in images[:5]:
            print(image.id)
            image.save()
            print(image.url, image.sha1)
            if not image.url:
                image.delete()
                print('delete because of missing url')

            if not image.sha1:
                image.delete()
                print('delete because of missing sha1')


def change_text_for_html():

    texts = Text.objects.filter(body__startswith='<p>&lt;')

    for text in texts:
        data = {
            'html': text.body,
            'position': text.position,
            'language': text.language,
            'placeholder': text.placeholder,
            'plugin_type': 'HtmlCMSPlugin',
        }

        HtmlPlugin.objects.create(
            **data
        )
        text.delete()

    texts = Text.objects.filter(body__contains='&lt;')

    text_dict = {
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
    }

    for text in texts:

        body = keymap_replace(text.body, text_dict)

        text.body = body
        text.save()


def delete_repeted_news(json_name: str='posts-lang.json'):
    # open posts-lang.json
    with open(settings.BASE_DIR + '/gobcl_cms/utils/' + json_name) as news:
        json_news = json.loads(news.read())

    for news in json_news:
        title = news.get('titulo', '')
        language = news.get('lang', 'es')

        if language == 'es-CL':
            continue

        article_translation = ArticleTranslation.objects.filter(
            title=title,
        )

        if not article_translation.exists():
            continue

        article_translation = article_translation.filter(language_code='es')

        if not article_translation.exists():
            continue

        activate('es')
        Article.objects.translated(title=title).delete()


def create_json_news():

    json_files = ('gobcl-posts.json', 'gobcl-posts-2.json',
                  'gobcl-posts-3.json',)

    json_output = []
    for json_file in json_files:
        with open(settings.BASE_DIR + '/' + json_file) as news:
            json_news = json.loads(news.read())
        for news in json_news:
            title = news.get('titulo', '')
            url = news.get('url', '')
            json_output.append(
                {
                    'titulo': title,
                    'url': url
                }
            )

    with open('posts.json', 'w') as f:
        json.dump(json_output, f)


def create_json_language():

    json_files = ('gobcl-posts-lang.json', 'gobcl-posts-lang-2.json',
                  'gobcl-posts-lang-3.json',)

    json_output = []
    for json_file in json_files:
        with open(settings.BASE_DIR + '/' + json_file) as news:
            json_news = json.loads(news.read())
        for news in json_news:
            title = news.get('titulo', '')[0]
            url = news.get('url', '')
            language = news.get('lang', '') or news.get('language', '')

            json_output.append(
                {
                    'titulo': title,
                    'url': url,
                    'lang': language,
                }
            )

    with open('gobcl_cms/utils/posts-lang.json', 'w') as f:
        json.dump(json_output, f)


def create_redirects(json_name: str='posts.json'):

    with open(settings.BASE_DIR + '/gobcl_cms/utils/' + json_name) as news:
        json_news = json.loads(news.read())

    site = get_current_site('')
    for news in json_news:
        new_path = ''
        title = news.get('titulo', '')[0]
        url = news.get('url', '')

        old_path = url

        language = 'es'
        activate('es')
        article = Article.objects.filter(translations__title=title)
        if not article.exists():
            language = 'en'
            activate('en')
            article = Article.objects.filter(translations__title=title)
            if not article.exists():
                continue

        article = article.first()
        new_path = article.get_absolute_url(language=language)

        try:
            Redirect.objects.get_or_create(
                site=site,
                old_path=old_path,
                defaults={
                    'new_path': new_path,
                }
            )
        except Exception as e:
            print(e)
            print('*' * 10)
            print('antigua url:', old_path)
            print('nueva url:', new_path)
            print('*' * 10)
            new_path = new_path.split('/')[1]
            print(new_path)
            new_path = '/{}/{}/'.format(
                new_path,
                article.pk,
            )
            try:
                Redirect.objects.get_or_create(
                    site=site,
                    old_path=old_path,
                    defaults={
                        'new_path': new_path,
                    }
                )
            except:
                pass
