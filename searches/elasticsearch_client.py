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
                    'name^99',
                    'title^99',
                    'description',
                    'url^98',
                    'lead_in^90',
                    'detail',
                    'tags^97',
                    'categories^96',
                    'categories_slug^96',
                ),
                fuzziness='AUTO',
            )
        )

        filter_by_language = (
            Q('match', language_code=self.language) |
            Q('match', language_code='ALL')
        )

        return search.query(
            function_score_query
        ).query(
            filter_by_language
        ).suggest(
            'suggestions',
            self.query,
            term={'field': 'name'}
        )

    def execute(self):
        return self.search()[:10000].execute()
