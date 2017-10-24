from rest_framework import viewsets

from .serializers import CommuneSerializer
from .models import Commune


class CommuneViewSet(viewsets.ReadOnlyModelViewSet):
    model = Commune
    serializer_class = CommuneSerializer
    filter_fields = ('region',)

    def get_queryset(self):
        return self.model.objects.filter(
            region__government_structure=self.request.government_structure
        )
