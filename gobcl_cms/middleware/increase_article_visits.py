from django.utils.deprecation import MiddlewareMixin

from gobcl_cms.models import ArticleCount
from aldryn_newsblog.models import Article


class IncreaseArticleVisits(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):

        article_slug = view_kwargs.get('slug', None)

        if article_slug:

            article = Article.objects.filter(
                translations__slug=article_slug,
            ).first()
    
            if not article:
                return

            article_count = ArticleCount.objects.get_or_create(
                article=article
            )[0]

            article_count.increase()
