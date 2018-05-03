from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError

from .elasticsearch_config import get_elasticsearch_url

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl import Q


class ElasticSearchClient:
    '''
    Elasticsearch client to connect to index data from GOBCL
    '''

    def __init__(self, query, language, index=None, *args, **kwargs):
        self.query = query
        self.index = index
        self.language = language

    def search(self):
        client = Elasticsearch(get_elasticsearch_url())
        search = Search(using=client, index=self.index)

        # Search query and change boost by field
        multi_match = MultiMatch(
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

        # Change priority in results depends boost document
        function_score = {
            'function_score': {
                'field_value_factor': {
                    'field': 'boost',
                },
                'boost_mode': 'multiply',
                'query': multi_match
            }
        }

        # Filter depends language code
        filter_by_language = (
            Q('match', language_code=self.language) |
            Q('match', language_code='ALL')
        )

        search_obj = search.query(
            function_score
        ).query(
            filter_by_language
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
            # Add highlight to fields
            'name',
            'title',
            'detail',
            'description',
            'lead_in'
            'detail',
            pre_tags='<strong>',
            post_tags='</strong>',
            type='unified',
            fragment_size=100,
            no_match_size=100,
            number_of_fragments=1,
        ).update_from_dict(
            # Collapse results depends url value
            {
                'collapse': {
                    'field': 'url'
                }
            }
        )
        return search_obj

    def execute(self):
        try:
            # Execute search in Elasticsearch with size 10000
            return self.search()[:10000].execute()
        except TransportError:
            return []
