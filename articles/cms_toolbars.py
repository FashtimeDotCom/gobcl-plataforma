# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _, override

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool

from .models import Article


@toolbar_pool.register
class ArticleToolbar(CMSToolbar):
    # watch_models must be a list, not a tuple
    # see https://github.com/divio/django-cms/issues/4135
    watch_models = [Article, ]
    supported_apps = ('articles',)

    def get_on_delete_redirect_url(self, article, language):
        with override(language):
            url = reverse(
                '{0}:article-list'.format(article.app_config.namespace))
        return url

    def add_article_detail_buttons(self, menu, article):
        publisher = self.toolbar.add_button_list(
            'Article publisher',
            side=self.toolbar.RIGHT,
        )

        url = reverse(
            'admin:articles_article_change',
            args=(article.pk, )
        )
        menu.add_modal_item(_('Edit this article'), url=url,
                            active=True)

        classes = []

        public = article.public

        if not public or public.updated_at < article.updated_at:
            classes.append('cms-btn-action')

        publish_url = reverse('articles:article_publish', args=(article.slug,),)

        if self.toolbar.edit_mode:
            button = publisher.add_button(
                _('Publish'),
                url=publish_url,
                active=False,
                disabled=False,
                extra_classes=classes,
            )

    def populate(self):
        user = getattr(self.request, 'user', None)
        try:
            view_name = self.request.resolver_match.view_name
        except AttributeError:
            view_name = None

        if user and view_name:
            # If we're on an Article detail page, then get the article
            if view_name == 'article_detail':
                kwargs = self.request.resolver_match.kwargs
                article = Article.objects.translated(
                    slug=kwargs['slug']
                )

                if self.toolbar.edit_mode:
                    article = article.get(is_draft=True)
                else:
                    article = article.get(is_draft=False)

            else:
                article = None

            menu = self.toolbar.get_or_create_menu(
                'articles',
                'Noticias'
            )

            change_article_perm = user.has_perm(
                'articles.change_article')
            delete_article_perm = user.has_perm(
                'articles.delete_article')
            add_article_perm = user.has_perm('articles.add_article')

            if change_article_perm:
                url = reverse('admin:articles_article_changelist')
                menu.add_sideframe_item(_('Article list'), url=url)

            if add_article_perm:
                url = reverse('admin:articles_article_add')
                menu.add_modal_item(_('Add new article'), url=url)

            if change_article_perm and article:
                self.add_article_detail_buttons(menu, article)

            if delete_article_perm and article:
                url = reverse(
                    'admin:articles_article_delete',
                    args=(article.pk, )
                )
                redirect_url = reverse('admin:articles_article_changelist')
                menu.add_modal_item(_('Delete this article'), url=url,
                                    on_close=redirect_url)
