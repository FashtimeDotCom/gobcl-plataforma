# models
from aldryn_categories.models import Category


def categories(request):
    """
    Includes the list of categories in the context
    """

    context = {
        'categories': Category.objects.order_by('article__count__visits')
    }

    return context
