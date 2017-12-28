from rest_framework import serializers

from .models import ChileAtiendeFile


class ChileAtiendeFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChileAtiendeFile
        fields = (
            'id',
        )

