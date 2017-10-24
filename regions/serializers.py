from rest_framework import serializers

from .models import Commune


class CommuneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Commune
        fields = (
            'id',
            'name',
            'region',
            'description',
            'email',
            'phone',
            'twitter',
            'url',
        )
