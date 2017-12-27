"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _

from base import views as base_views
from users.urls import callback_pattern


urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    url(r'^api/1.0/', include('api.urls')),
    url(r'^admin/', include('loginas.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('users.urls')),
    url(r'^api/1.0/', include('api.urls')),
    url(r'^$', base_views.IndexTemplateView.as_view(), name='home'),
    url(r'^callback/', include(callback_pattern)),
    url(_(r'^about/$'), base_views.AboutTemplateView.as_view(), name='about'),
    url(_(r'^about-interior/$'),
        base_views.AboutInteriorTemplateView.as_view(), name='about_interior'),
    url(_(r'^institutions/'), include('institutions.urls')),
    url(_(r'^regions/'), include('regions.urls')),
    url(_(r'^ministries/'), include('ministries.urls')),
    url(_(r'^search/'), include('searches.urls')),
    url(_(r'^procedures/'), include('services.urls')),
    url(_(r'^'), include('cms.urls')),
    prefix_default_language=False,
)

if settings.DEBUG or settings.TRAVIS or settings.DOCKER:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

if settings.TEST:
    urlpatterns += [
        url(r'^campaigns/', include('campaigns.urls'), name='campaigns'),
    ]
