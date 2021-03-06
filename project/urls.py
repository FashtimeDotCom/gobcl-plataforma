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

from users.urls import callback_pattern


urlpatterns = [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^', include('gobcl_cms.news_urls')),
]

urlpatterns += i18n_patterns(
    url(_(r'^news/'), include('articles.urls'), name='articles'),
    url(_(r'^news/'), include('gobcl_cms.news_urls')),
    url(r'^api/1.0/', include('api.urls')),
    url(r'^admin/', include('loginas.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('users.urls')),
    url(r'^api/1.0/', include('api.urls')),
    url(r'^callback/', include(callback_pattern)),
    url(_(r'^institutions/'), include('institutions.urls')),
    url(_(r'^regions/'), include('regions.urls')),
    url(_(r'^ministries/'), include('ministries.urls')),
    url(_(r'^search/'), include('searches.urls')),
    url(_(r'^procedures/'), include('services.urls')),
    url(_(r'^articles/'), include('gobcl_cms.urls')),
    url(r'^', include('cms.urls')),
    prefix_default_language=False,
)

if settings.TEST or settings.TRAVIS:
    urlpatterns += [
        url(r'^campaigns/', include('campaigns.urls'), name='campaigns'),
        url(r'^streams/', include('streams.urls'), name='streams'),
        url(r'^', include('gobcl_cms.index_urls')),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

# custom error pages
handler400 = 'base.views.bad_request_view'
handler403 = 'base.views.permission_denied_view'
handler404 = 'base.views.page_not_found_view'
handler500 = 'base.views.server_error_view'
