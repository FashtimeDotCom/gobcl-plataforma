# standard
import copy

# models
from hitcount.models import HitCount
from django.core.cache import caches


def most_visited_urls():
    """
    Constructs a list of pages which correspond
    to the most visited urls on this site, using HitCount.
    """
    pages = HitCount.objects.filter()[:6]
    pages_list = []
    for page in pages:
        base_dict = page.__dict__
        page_dict = copy.deepcopy(base_dict)
        page_dict['content_object'] = page.content_object
        pages_list.append(page_dict)

    return pages_list


def get_most_visited_urls(request):
    """
    Returns a dictionary with a list of the most visited urls.
    List is obtained by searching the cache.
    If cache has no key for most_visited_urls it will
    call most_visited_urls() and set it to the cache.
    """
    cache = caches['default']
    most_visited_urls_cache = cache.get('most_visited_urls')
    if not most_visited_urls_cache:
        most_visited_urls_cache = cache.set(
            'most_visited_urls',
            most_visited_urls(),
            86400,
        )

    return {'most_visited_urls': most_visited_urls_cache}
