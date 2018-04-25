# # standard library
import warnings

# django
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseBadRequest
from django.http import HttpResponseForbidden
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.clickjacking import xframe_options_sameorigin

# cms
from aldryn_newsblog.admin import ArticleAdmin as BaseArticleAdmin
from aldryn_newsblog.admin import ArticleAdminForm as BaseArticleAdminForm
from aldryn_newsblog.models import Article
from aldryn_people.models import Group
from aldryn_people.models import Person
from cms import operations
from cms.admin.forms import PluginAddValidationForm
from cms.admin.placeholderadmin import _instance_overrides_method
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from cms.models.pluginmodel import CMSPlugin
from cms.plugin_pool import plugin_pool

# models
from .models import ArticleCount
from .models import HeaderImage


# Register your models here.
admin.site.unregister(Article)
admin.site.unregister(Group)
admin.site.unregister(Person)


class ArticleAdminForm(BaseArticleAdminForm):
    """
    Override ArticleAdminForm to remove related field
    """
    class Meta:
        model = Article
        fields = [
            'app_config',
            'categories',
            'featured_image',
            'is_featured',
            'is_published',
            'lead_in',
            'meta_description',
            'meta_keywords',
            'meta_title',
            'owner',
            'slug',
            'tags',
            'title',
        ]


class ArticleAdmin(BaseArticleAdmin):
    """
    Override ArticleAdmin to remove related field
    Also call prefetch related on the translations
    """
    form = ArticleAdminForm
    list_display = ('title', 'publishing_date', 'is_featured', 'is_published')
    search_fields = (
        'translations__title',
    )

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'author',
                'publishing_date',
                'is_published',
                'is_featured',
                'featured_image',
                'lead_in',
            )
        }),
        (_('Meta Options'), {
            'classes': ('collapse',),
            'fields': (
                'slug',
                'meta_title',
                'meta_description',
                'meta_keywords',
            )
        }),
        (_('Advanced Settings'), {
            'classes': ('collapse',),
            'fields': (
                'tags',
                'categories',
                'owner',
                'app_config',
            )
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('translations')

    @xframe_options_sameorigin
    def add_plugin_after(self, request):
        """
        Shows the add plugin form and saves it on POST.

        Requires the following GET parameters:
            - cms_path
            - placeholder_id
            - plugin_type
            - plugin_language
            - plugin_parent (optional)
            - plugin_position (optional)
        """
        import ipdb
        ipdb.set_trace()
        print('whut')
        form = PluginAddValidationForm(request.GET)

        if not form.is_valid():
            # list() is necessary for python 3 compatibility.
            # errors is s dict mapping fields to a list of errors
            # for that field.
            error = list(form.errors.values())[0][0]
            return HttpResponseBadRequest(force_text(error))

        plugin_data = form.cleaned_data
        placeholder = plugin_data['placeholder_id']
        plugin_type = plugin_data['plugin_type']

        if not self.has_add_plugin_permission(
            request, placeholder, plugin_type
        ):
            message = force_text(
                _('You do not have permission to add a plugin')
            )
            return HttpResponseForbidden(message)

        parent = plugin_data.get('plugin_parent')

        if parent:
            position = parent.cmsplugin_set.count()
        else:
            position = CMSPlugin.objects.filter(
                parent__isnull=True,
                language=plugin_data['plugin_language'],
                placeholder=placeholder,
            ).count()

        plugin_data['position'] = position

        plugin_class = plugin_pool.get_plugin(plugin_type)
        plugin_instance = plugin_class(plugin_class.model, self.admin_site)

        # Setting attributes on the form class is perfectly fine.
        # The form class is created by modelform factory every time
        # this get_form() method is called.
        plugin_instance._cms_initial_attributes = {
            'language': plugin_data['plugin_language'],
            'placeholder': plugin_data['placeholder_id'],
            'parent': plugin_data.get('plugin_parent', None),
            'plugin_type': plugin_data['plugin_type'],
            'position': plugin_data['position'],
        }

        response = plugin_instance.add_view(request)

        plugin = getattr(plugin_instance, 'saved_object', None)

        uses_hook = _instance_overrides_method(
            PlaceholderAdminMixin,
            self,
            'post_add_plugin'
        )

        if plugin_instance.object_successfully_changed and uses_hook:
            warnings.warn('The post_add_plugin hook has been deprecated. '
                          'Please use placeholder operation signals instead.',
                          DeprecationWarning)
            self.post_add_plugin(request, plugin)

        if plugin_instance._operation_token:
            tree_order = placeholder.get_plugin_tree_order(plugin.parent_id)
            self._send_post_placeholder_operation(
                request,
                operation=operations.ADD_PLUGIN,
                token=plugin_instance._operation_token,
                plugin=plugin,
                placeholder=plugin.placeholder,
                tree_order=tree_order,
            )
        return response

    def get_urls(self):
        """
        Register the plugin specific urls (add/edit/copy/remove/move)
        """
        info = "%s_%s" % (
            self.model._meta.app_label,
            self.model._meta.model_name
        )

        def pat(regex, fn):
            return url(
                regex,
                self.admin_site.admin_view(fn),
                name='%s_%s' % (info, fn.__name__)
            )

        url_patterns = [
            pat(r'add-plugin/after/$', self.add_plugin_after),
        ]
        return url_patterns + super(PlaceholderAdminMixin, self).get_urls()


admin.site.register(Article, ArticleAdmin)


@admin.register(ArticleCount)
class ArticleCountAdmin(admin.ModelAdmin):
    list_display = (
        'article',
        'visits',
    )
    readonly_fields = (
        'article',
        'visits',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeaderImage)
class HeaderImage(admin.ModelAdmin):
    list_display = (
        'name',
        'is_active',
    )
    list_filter = (
        'is_active',
    )
