from rest_framework import serializers

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

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
    featured_image = ThumbnailSerializer()

    class Meta:
        model = Article
        fields = (
            'id',
            'translations',
            'featured_image',
            'publishing_date',
            'url',
        )
