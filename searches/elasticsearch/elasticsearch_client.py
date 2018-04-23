from elasticsearch import Elasticsearch

from .elasticsearch_config import get_elasticsearch_url

from elasticsearch_dsl import Search
from elasticsearch_dsl import Q


class ElasticSearchClient:

    def __init__(self, query, language, index=None, *args, **kwargs):
        self.query = query
        self.index = index
        self.language = language

    def search(self):
        client = Elasticsearch(get_elasticsearch_url())
        search = Search(using=client, index=self.index)

        function_score_query = Q(
            'function_score',
            query=Q(
                'multi_match',
                query=self.query,
                fields=(
                    'name^4',
                    'title^4',
                    'description',
                    'url^3',
                    'lead_in^2',
                    'detail',
                    'tags^2',
                    'categories^2',
                    'categories_slug^2',
                ),
                fuzziness='AUTO',
            )
        )

        filter_by_language = (
            Q('match', language_code=self.language) |
            Q('match', language_code='ALL')
        )

        search_obj = search.query(
            function_score_query
        ).query(
            filter_by_language
        ).highlight(
            fields='_all',
            pre_tags='<strong>',
            post_tags='</strong>',
        ).suggest(
            'suggestion_name',
            self.query,
            term={
                'field': 'name'
            }
        ).suggest(
            'suggestion_title',
            self.query,
            term={
                'field': 'title'
            }
        ).highlight(
            'name',
            'title',
            'detail',
            'description',
            'lead_in'
            'detail',
            pre_tags='<strong>',
            post_tags='</strong>',
            type='plain',
            fragment_size=100,
            no_match_size=100,
            number_of_fragments=1,
        )

        return search_obj

    def execute(self):
        return self.search()[:10000].execute()
