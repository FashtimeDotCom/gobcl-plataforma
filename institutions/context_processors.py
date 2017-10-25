from ministries.models import Ministry


def most_visited_urls(request):
    """  """

    context = {
        'most_visited_urls': Ministry.objects.filter(
            government_structure=request.government_structure
        )[:6]
    }

    return context
