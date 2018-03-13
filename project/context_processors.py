from django.conf import settings


def show_google_analytics(request):
    return {
        'show_google_analytics': settings.SHOW_GOOGLE_ANALYTICS
    }
