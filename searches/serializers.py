from rest_framework import serializers

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from cms.utils.i18n import get_current_language
from django.utils.translation import get_language

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from aldryn_newsblog.models import Article


class ThumbnailSerializer(serializers.ImageField):

    def to_representation(self, instance):
        return thumbnail_url(instance.file, 'new_list_item')


class ArticleSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Article)
    url = serializers.ReadOnlyField(
        source='get_absolute_url',
    )
    alt_image = serializers.ReadOnlyField(
        source='featured_image.default_alt_text',
    )
    featured_image = ThumbnailSerializer()
    current_language = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'id',
            'translations',
            'featured_image',
            'publishing_date',
            'url',
            'alt_image',
            'current_language',
        )
    
    def get_current_language(self, obj):
        language = get_language()
        return language
