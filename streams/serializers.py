from rest_framework import serializers

from parler_rest.fields import TranslatedFieldsField
from parler_rest.serializers import TranslatableModelSerializer

from .models import Stream
from .models import StreamEvent


class StreamEventSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=StreamEvent)

    class Meta:
        model = StreamEvent
        fields = (
            'id',
            'translations',
            'date_time',
        )


class StreamSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Stream)
    events = serializers.SerializerMethodField()
    current_language = serializers.SerializerMethodField()

    class Meta:
        model = Stream
        fields = (
            'id',
            'current_language',
            'translations',
            'url',
            'get_url',
            'events',
        )

    def get_events(self, obj):
        events = obj.events
        request = self.context.get('request')
        serializer = StreamEventSerializer(
            events, many=True, context={
                'request': request})
        return serializer.data

    def get_current_language(self, obj):
        request = self.context.get('request')
        return request.LANGUAGE_CODE
