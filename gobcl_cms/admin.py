from aldryn_newsblog.admin import ArticleAdmin as BaseArticleAdmin
from aldryn_newsblog.admin import ArticleAdminForm as BaseArticleAdminForm
from aldryn_newsblog.models import Article
from aldryn_people.models import Group
from aldryn_people.models import Person
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

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
    list_display = ('title', 'slug', 'is_featured', 'is_published')

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


admin.site.register(Article, ArticleAdmin)
