from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework import status
from rest_framework.response import Response

from .models import Stream

from .serializers import StreamSerializer
from .serializers import StreamEventSerializer


class StreamViewSet(viewsets.ReadOnlyModelViewSet):
    model = Stream
    serializer_class = StreamSerializer

    def get_queryset(self):
        queryset = Stream.objects.active()
        queryset = queryset.prefetch_related(
            'events',
            'translations',
            'events__translations',
        )
        return queryset

    @detail_route(methods=['get'])
    def events(self, request, pk=None):
        stream = self.get_object()
        events = stream.events

        serializer = StreamEventSerializer(
            events,
            context={
                'request': request
            }
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )
