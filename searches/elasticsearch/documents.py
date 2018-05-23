from .elasticsearch_config import get_elasticsearch_url

from elasticsearch.exceptions import NotFoundError
from elasticsearch.exceptions import TransportError
from elasticsearch.exceptions import ConnectionError

from elasticsearch_dsl import DocType
from elasticsearch_dsl import Text
from elasticsearch_dsl import Integer
from elasticsearch_dsl import Index
from elasticsearch_dsl import connections
from elasticsearch_dsl import analyzer
from elasticsearch_dsl import token_filter
from elasticsearch_dsl import Keyword


connections.create_connection(
    hosts=[get_elasticsearch_url()],
    timeout=20
)


# government_structure = GovernmentStructure.get_government()


class SearchIndex(DocType):
    '''
    Generic Document to index GOBCL
    '''

    name = Text(
        store=True,
        copy_to='suggest_field'
    )
    title = Text(
        store=True,
        copy_to='suggest_field'
    )
    description = Text(
        store=True
    )
    language_code = Text()
    url = Keyword()
    lead_in = Text(
        fields={'raw': Keyword()},
        store=True
    )
    detail = Text(
        store=True,
        copy_to='suggest_field'
    )
    tags = Text()
    categories = Text()
    categories_slug = Text()
    boost = Integer()
    suggest_field = Text()

    class Meta:
        # Name of index
        index = 'searches'

    def save(self, **kwargs):
        """
        Set document id to {classname}-{object.id}-{object.language_code}
        """
        # Get the obj parameter, and remove it from kwargs
        obj = kwargs.pop('obj', None)
        if obj is not None:
            self.meta.id = obj.get_elasticsearch_id()

        try:
            super(SearchIndex, self).save(**kwargs)
        except (TransportError, ConnectionError):
            pass

    def delete(self, **kwargs):
        try:
            super(SearchIndex, self).delete(**kwargs)
        except (TransportError, ConnectionError):
            pass

    @classmethod
    def get(cls, id, **kwargs):
        try:
            super(SearchIndex, cls).get(id, **kwargs)
        except (TransportError, ConnectionError):
            pass

    @classmethod
    def init_index(cls):
        '''
        Class method to init index
        '''

        # default analyzer
        shingle_filter = token_filter(
            'shingle_filter',
            type='shingle',
            min_shingle_size=2,
            max_shingle_size=3,
        )
        default_analyzer = analyzer(
            'default',
            tokenizer='standard',
            char_filter=['html_strip'],
            filter=['lowercase', 'asciifolding', shingle_filter]
        )

        # set the analyzers for the available languages
        # TODO: languages and languages_stopwords should be in settings
        languages = ('es', 'en')
        languages_stopwords = {
            'en': '_english_',
            'es': '_spanish_',
        }
        languages_analyzers = {}
        languages_filters = {}
        for language in languages:
            languages_filters[language] = token_filter(
                language + '_filter',
                type='stop',
                stopwords=languages_stopwords[language],
            )
            languages_analyzers[language] = analyzer(
                language + '_analyzer',
                tokenizer='standard',
                char_filter=['html_strip'],
                filter=['lowercase', 'asciifolding', languages_filters[language]]
            )

        # Add analyzers, the index has to be closed before any configuration
        searches_index = Index('searches')
        # default analyzer
        searches_index.analyzer(default_analyzer)
        # languages search analyzers
        for language in languages:
            searches_index.analyzer(languages_analyzers[language])
        searches_index.save()

        # create the mappings in elasticsearch
        cls.init()

    @classmethod
    def delete_all(cls):
        '''
        Class method to delete Index
        '''
        try:
            return Index('searches').delete()
        except NotFoundError:
            pass
