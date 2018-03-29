from rest_framework import serializers

from parler_rest.fields import TranslatedFieldsField

from .models import Contingency
from .models import ContingencyEvent
from .models import ContingencyInformation


class ContingencySerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(shared_model=Contingency)
    events = serializers.ReadOnlyField(source='get_contingency_event_api_url')
    informations = serializers.ReadOnlyField(
        source='get_contingency_information_api_url')

    class Meta:
        model = Contingency
        fields = (
            'id',
            'translations',
            'events',
            'informations',
        )


class ContingencyEventSerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(shared_model=ContingencyEvent)

    class Meta:
        model = ContingencyEvent
        fields = (
            'id',
            'translations',
            'url',
            'date_time',
        )


class ContingencyInformationSerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(shared_model=ContingencyInformation)

    class Meta:
        model = ContingencyInformation
        fields = (
            'id',
            'translations',
            'url',
        )
