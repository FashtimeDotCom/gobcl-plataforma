# django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# models
from campaigns.models import Campaign


def paginate(request, objects, page_size=25):
    paginator = Paginator(objects, page_size)
    page = request.GET.get('p')

    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_objects = paginator.page(paginator.num_pages)

    return paginated_objects


def clean_query_string(request):
    clean_query_set = request.GET.copy()

    clean_query_set = dict(
        (k, v) for k, v in request.GET.items() if k != 'o'
    )

    try:
        del clean_query_set['p']
    except KeyError:
        pass

    mstring = []
    for key in clean_query_set.keys():
        valuelist = request.GET.getlist(key)
        mstring.extend(['%s=%s' % (key, val) for val in valuelist])

    return '&'.join(mstring)


def get_home_campaigns(request):
    campaigns = Campaign.objects.active()
    campaigns = campaigns.prefetch_related('translations')

    featured_campaigns = campaigns.filter(is_featured=True)
    non_featured_campaigns = campaigns.filter(is_featured=False)

    return {
        'featured_campaigns': featured_campaigns,
        'campaigns': non_featured_campaigns,
        'show_featured_on_normal': not featured_campaigns.exists(),
    }
