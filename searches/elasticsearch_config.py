from django.conf import settings


def get_elasticsearch_url():
    elasticsearch_config = settings.ELASTICSEARCH_DSL
    return '{}:{}'.format(
        elasticsearch_config.get('HOST'),
        elasticsearch_config.get('PORT'),
    )
