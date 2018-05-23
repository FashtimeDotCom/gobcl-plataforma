# django
from django.core.management.base import BaseCommand

# elasticsearch
from searches.elasticsearch.search import bulk_index


class Command(BaseCommand):
    help = 'Rebuilds the elasticsearch index'

    def handle(self, *args, **options):
        bulk_index()
