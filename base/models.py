# -*- coding: utf-8 -*-
""" Models for the base application.

All apps should use the BaseModel as parent for all models
"""

# standard library
import json

# django
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# elasticsearch
from searches.elasticsearch.documents import SearchIndex

# base
from base import utils
from base.managers import BaseManager, BaseGovernmentQuerySet
from base.serializers import ModelEncoder

# utils
from base.utils import remove_tags


# public methods
def file_path(self, name):
    """
    Generic method to give to a FileField or ImageField in it's upload_to
    parameter.

    This returns the name of the class, concatenated with the id of the
    object and the name of the file.
    """
    base_path = "{}/{}/{}"

    return base_path.format(
        self.__class__.__name__,
        utils.random_string(30),
        name
    )


class BaseModel(models.Model):
    """ An abstract class that every model should inherit from """
    BOOLEAN_CHOICES = ((False, _('No')), (True, _('Yes')))

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("creation date"),
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True,
        help_text=_("edition date"),
    )

    # using BaseManager
    objects = BaseManager()

    class Meta:
        """ set to abstract """
        abstract = True

    # public methods
    def update(self, **kwargs):
        """ proxy method for the QuerySet: update method
        highly recommended when you need to save just one field

        """
        kwargs['updated_at'] = timezone.now()

        for kw in kwargs:
            self.__setattr__(kw, kwargs[kw])

        self.__class__.objects.filter(pk=self.pk).update(**kwargs)

    def to_dict(instance, fields=None, exclude=None):
        """
        Returns a dict containing the data in ``instance``

        ``fields`` is an optional list of field names. If provided, only the
        named fields will be included in the returned dict.

        ``exclude`` is an optional list of field names. If provided, the named
        fields will be excluded from the returned dict, even if they are listed
        in the ``fields`` argument.
        """

        opts = instance._meta
        data = {}
        for f in opts.fields + opts.many_to_many:
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, models.fields.related.ManyToManyField):
                # If the object doesn't have a primary key yet, just use an
                # emptylist for its m2m fields. Calling f.value_from_object
                # will raise an exception.
                if instance.pk is None:
                    data[f.name] = []
                else:
                    # MultipleChoiceWidget needs a list of pks, not objects.
                    data[f.name] = list(
                        f.value_from_object(instance).values_list('pk',
                                                                  flat=True))
            else:
                data[f.name] = f.value_from_object(instance)
        return data

    def to_json(self, fields=None, exclude=None, **kargs):
        """
        Returns a string containing the data in of the instance in json format

        ``fields`` is an optional list of field names. If provided, only the
        named fields will be included in the returned dict.

        ``exclude`` is an optional list of field names. If provided, the named
        fields will be excluded from the returned dict, even if they are listed
        in the ``fields`` argument.

        kwargs are optional named parameters for the json.dumps method
        """
        # obtain a dict of the instance data
        data = self.to_dict(fields=fields, exclude=exclude)

        # turn the dict to json
        return json.dumps(data, cls=ModelEncoder, **kargs)

    def get_full_url(self):
        absolute_url = self.get_absolute_url()
        site = Site.objects.get_current().domain
        return 'https://{site}{path}'.format(site=site, path=absolute_url)

    def get_elasticsearch_id(self, language_code=None):
        if language_code is None:
            language_code = 'ALL'
            if hasattr(self, 'language_code'):
                language_code = self.language_code
        return (
            str(type(self).__name__) + '-' +
            str(self.id) + '-' +
            language_code
        )

    def get_elasticsearch_doc(self, language_code=None):
        """
        Returns the elasticsearch index corresponding to that document, returns
        None if it doesn't exist
        """
        return SearchIndex.get(
            id=self.get_elasticsearch_id(language_code=language_code),
            ignore=404
        )

    def get_elasticsearch_kwargs(self):
        """
        Returns the arguments that should be pass when creating the
        elasticearch document
        """
        kwargs = {}
        if hasattr(self, 'name'):
            kwargs['name'] = self.name
        if hasattr(self, 'title'):
            kwargs['title'] = self.title
        if hasattr(self, 'description'):
            kwargs['description'] = remove_tags(self.description)
        if hasattr(self, 'language_code'):
            kwargs['language_code'] = self.language_code
        else:
            kwargs['language_code'] = 'ALL'
        kwargs['url'] = self.get_absolute_url()
        # kwargs['boost'] = boost

        return kwargs

    def index_in_elasticsearch(self, boost=1):
        """
        Indexes a document in elasticearch with the info of this object
        """
        kwargs = self.get_elasticsearch_kwargs()
        doc = SearchIndex(boost=boost, **kwargs)
        doc.save(obj=self)

    def deindex_in_elasticsearch(self):
        """
        Deletes the elasticsearch document related to this object if it exists
        """
        languages = ('es', 'en', 'ALL')
        for language in languages:
            doc = self.get_elasticsearch_doc(language_code=language)

            if doc is not None:
                doc.delete()

    def reindex_in_elasticsearch(self):
        """
        Deletes index document and index it again, it document doesn't exists,
        it's the same as index_in_elasticsearch
        """
        # TODO: fix boosts
        self.deindex_in_elasticsearch()
        self.index_in_elasticsearch(1)

    def delete(self, *args, **kwargs):
        """
        Override this method to delete the corresponding elasticsearch document
        when deleting the object
        """
        self.deindex_in_elasticsearch()
        super(BaseModel, self).delete(*args, **kwargs)


def lastest_government_structure():
    from government_structures.models import GovernmentStructure
    government_structure = GovernmentStructure.objects.order_by(
        'publication_date').last()
    if government_structure:
        return government_structure.pk
    return


class BaseGovernmentStructureModel(BaseModel):
    government_structure = models.ForeignKey(
        'government_structures.GovernmentStructure',
        verbose_name=_('government structure'),
        default=lastest_government_structure,
    )

    objects = BaseGovernmentQuerySet.as_manager()

    class Meta:
        """ set to abstract """
        abstract = True
