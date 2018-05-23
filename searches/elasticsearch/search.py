import re

from abc import ABCMeta, abstractmethod

from django.utils.formats import date_format
from django.utils.translation import activate

from elasticsearch_dsl import IndexTemplate
from elasticsearch_dsl import Index
from searches.elasticsearch.documents import SearchIndex

# models
from government_structures.models import GovernmentStructure
from ministries.models import Ministry
from links.models import FooterLink
from campaigns.models import Campaign
from ministries.models import PublicService
from presidencies.models import Presidency
from articles.models import Article
from public_servants.models import PublicServant
from regions.models import Region
from sociocultural_departments.models import SocioculturalDepartment
from public_enterprises.models import PublicEnterprise
from cms.models.pagemodel import Page


def remove_tags(text):
    '''
    Function to remove HTML tags
    '''
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)


def bulk_index():
    index_class = SearchIndex

    index_class.delete_all()
    index_class.init_index()

    # index models and assign boost for them
    print('public articles')
    Article.objects.bulk_index()

    # TODO: Why?
    activate('es')

    government_structure = GovernmentStructure.get_government()

    print('presidency')
    Presidency.objects.bulk_index(4, government_structure=government_structure)
    print('sociocultural department',)
    SocioculturalDepartment.objects.bulk_index(2, government_structure=government_structure)
    print('public enterprises')
    PublicEnterprise.objects.bulk_index(1.5, government_structure=government_structure)
    print('regions')
    Region.objects.bulk_index(1.3, government_structure=government_structure)
    print('public servant')
    PublicServant.objects.bulk_index(3, government_structure=government_structure)
    print('public services')
    PublicService.objects.bulk_index(1.5, government_structure=government_structure)
    print('campaigns')
    Campaign.objects.bulk_index()
    print('footer links')
    FooterLink.objects.bulk_index(1.2, government_structure=government_structure)
    print('ministries')
    Ministry.objects.bulk_index(2, government_structure=government_structure)