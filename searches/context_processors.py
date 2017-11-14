from aldryn_newsblog.models import Article


def get_feature_news(request):

    feature_news = {
        'feature_news': Article.objects.filter(
            is_featured=True
        ).published().prefetch_related('categories')[:3]
    }

    return feature_news
