from rest_framework import serializers

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from aldryn_newsblog.models import Article


class ThumbnailSerializer(serializers.ImageField):

    def to_representation(self, instance):
        if not instance:
            return ''
        return thumbnail_url(instance.file, 'new_list_item')


class TranslationField(TranslatedFieldsField):

    def to_representation(self, value):
        if isinstance(value, dict):
            return value
        return super(TranslationField, self).to_representation(value)


class ArticleSerializer(TranslatableModelSerializer):

    translations = TranslationField(shared_model=Article)
    url = serializers.URLField(
        source='get_absolute_url',
    )
    alt_image = serializers.SerializerMethodField()
    featured_image = ThumbnailSerializer()

    class Meta:
        model = Article
        fields = (
            'id',
            'featured_image',
            'publishing_date',
            'url',
            'alt_image',
            'translations',
        )

    def get_alt_image(self, obj):

        if not obj.featured_image_id:
            return ''

        alt_text = obj.featured_image.default_alt_text
        return alt_text or ''
