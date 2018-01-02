# standard
import copy

# django
from django.core.cache import caches

# models
from aldryn_newsblog.models import Article


def featured_news():
    """
    Returns a list of the 3 featured articles.
    """
    articles = Article.objects.filter(
        is_featured=True
    ).published().prefetch_related(
        'categories'
    )[:3]

    featured_news_list = []

    for article in articles:
        base_dict = article.__dict__
        article_dict = copy.copy(base_dict)
        article_dict['title'] = article.title
        article_dict['categories'] = article.categories.all()
        article_dict['get_absolute_url'] = article.get_absolute_url()
        featured_news_list.append(article_dict)

    return featured_news_list


def get_featured_news(request):
    """
    Returns a dictionary with a list of featured news.
    List is obtained by searching the cache.
    If cache has no key for featured_news it will call
    featured_news() and set it to the cache.
    """
    cache = caches['default']
    featured_news_cache = cache.get('featured_news')
    if not featured_news_cache:
        cache.set(
            'featured_news',
            featured_news(),
            86400,
        )
        featured_news_cache = cache.get('featured_news')

    return {'featured_news': featured_news_cache}
