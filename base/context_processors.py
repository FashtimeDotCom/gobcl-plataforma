# models
from aldryn_categories.models import Category


def categories(request):
    """
    Includes the list of categories in the context
    """

    category_ids = list(set(Category.objects.order_by(
        'article__count__visits'
    ).values_list('id', flat=True)))

    context = {
        'categories': Category.objects.filter(id__in=category_ids)[:5]
    }

    return context
