# models
from aldryn_categories.models import Category


def categories(request):
    """
    Includes the list of categories in the context
    """

    category_ids = Category.objects.order_by(
        'article__count__visits'
    ).values('id')

    context = {
        'categories': Category.objects.filter(id__in=category_ids)[:5]
    }

    return context
