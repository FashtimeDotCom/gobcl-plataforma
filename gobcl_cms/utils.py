from djangocms_text_ckeditor.models import Text
from djangocms_picture.models import Picture


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
