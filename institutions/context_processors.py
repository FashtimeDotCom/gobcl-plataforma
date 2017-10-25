# models
from hitcount.models import HitCount
from ministries.models import Ministry
from regions.models import Region


def most_visited_urls(request):
    context = {
        'most_visited_urls': HitCount.objects.filter()[:6]
    }

    return context
