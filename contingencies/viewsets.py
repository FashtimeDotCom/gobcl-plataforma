from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from .serializers import ContingencySerializer
from .serializers import ContingencyEventSerializer
from .serializers import ContingencyInformationSerializer

from .models import Contingency


class ContingencyViewSet(viewsets.ReadOnlyModelViewSet):
    model = Contingency
    serializer_class = ContingencySerializer

    def get_queryset(self):
        return self.model.objects.active()

    @detail_route(methods=['get'])
    def events(self, request, pk=None):
        contingency = self.get_object()
        serializer = ContingencyEventSerializer(
            contingency.events.all(),
            many=True,
        )
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def informations(self, request, pk=None):
        contingency = self.get_object()
        serializer = ContingencyInformationSerializer(
            contingency.informations.all(),
            many=True,
        )
        return Response(serializer.data)
