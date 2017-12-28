from djangocms_text_ckeditor.models import Text
from djangocms_picture.models import Picture

from aldryn_newsblog.models import Article
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
