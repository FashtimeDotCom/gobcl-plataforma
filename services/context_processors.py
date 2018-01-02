# standard
import copy

# django
from django.core.cache import caches

# models
from .models import ChileAtiendeFile


def chile_atiende_files():
    """
    Returns a list of 6 ChileAtiendeFile.
    """

    chile_atiende_files = ChileAtiendeFile.objects.all()[:6]
    chile_atiende_files_list = []
    for chile_atiende_file in chile_atiende_files:
        base_dict = chile_atiende_file.__dict__
        file_dict = copy.copy(base_dict)
        file_dict['get_absolute_url'] = chile_atiende_file.get_absolute_url()
        chile_atiende_files_list.append(file_dict)

    return chile_atiende_files_list


def get_chile_atiende_files(request):
    """
    Returns a dictionary with a list of ChileAtiendeFile.
    List is obtained by searching the cache.
    If cache has no key for chile_atiende_files it will call
    chile_atiende_files() and set it to the cache.
    """
    cache = caches['default']
    chile_atiende_files_cache = cache.get('chile_atiende_files')
    if not chile_atiende_files_cache:
        cache.set(
            'chile_atiende_files',
            chile_atiende_files(),
            86400,
        )
        chile_atiende_files_cache = cache.get('chile_atiende_files')

    return {
        'chile_atiende_files': chile_atiende_files_cache
    }
