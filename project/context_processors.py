from django.conf import settings


def show_analytics_config(request):
    return {
        'show_google_analytics': settings.SHOW_GOOGLE_ANALYTICS,
        'show_hotjar': settings.SHOW_HOTJAR,
    }
