from rest_framework import serializers

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from aldryn_newsblog.models import Article


class ArticleSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Article)
    url = serializers.ReadOnlyField(
        source='get_absolute_url',
    )

    class Meta:
        model = Article
        fields = (
            'id',
            'translations',
            'publishing_date',
            'url',
        )
