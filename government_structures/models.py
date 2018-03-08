# -*- coding: utf-8 -*-
""" Models for the government_structures application. """
# standard library
import copy

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# models
from base.models import BaseModel


class GovernmentStructure(BaseModel):
    publication_date = models.DateTimeField(
        _('publication date'),
        unique=True,
    )
    current_government = models.BooleanField(
        _('current government'),
        default=False,
    )

    class Meta:
        verbose_name = _('government structure')
        verbose_name_plural = _('government structures')
        permissions = (
            ('view_government_structure', _('Can view government structures')),
        )

    def __str__(self):
        return '{}'.format(self.publication_date)

    def save(self, **kwargs):
        # Make sure the default government are unique
        if self.current_government:
            GovernmentStructure.objects.filter(
                current_government=True,
            ).update(
                current_government=False,
            )
        super(GovernmentStructure, self).save(**kwargs)

    @classmethod
    def get_government(cls, date=None):
        if not date:
            return cls.objects.get_or_none(current_government=True)

    def _duplicate(self, date, with_public_servants=True):

        government_structures = GovernmentStructure.objects.filter(
            publication_date=date)
        if government_structures.exists():
            return

        government_structure = copy.copy(self)
        government_structure.id = None
        government_structure.current_government = False
        government_structure.publication_date = date
        government_structure.save()

        for field in self._meta.fields_map.values():

            if not with_public_servants:
                if field.name == 'publicservant':
                    continue

            model = field.related_model
            objects = model.objects.filter(government_structure=self)
            for obj in objects:
                new_obj = copy.copy(obj)

                # check for and copy translations in model
                if hasattr(new_obj, 'translations'):
                    translations = copy.copy(new_obj.translations.all())
                else:
                    translations = None

                new_obj.id = None
                new_obj.government_structure = government_structure
                new_obj.save()

                # save new translations
                if translations:
                    for translation in translations:
                        translation.id = None
                        translation.master_id = new_obj.id
                        translation.save()

            # for f in field.related_model._meta.fields_map.values():

            #     if not with_public_servants:
            #         if f.name == 'publicservant':
            #             continue

            #     model = f.related_model
            #     objects = model.objects.filter(government_structure=self)
            #     for obj in objects:
            #         new_obj = copy.copy(obj)

            #         # check for and copy translations in model
            #         if hasattr(new_obj, 'translations'):
            #             translations = copy.copy(new_obj.translations.all())
            #         else:
            #             translations = None

            #         new_obj.id = None
            #         if hasattr(new_obj, 'government_structure'):
            #             new_obj.government_structure = government_structure
            #         new_obj.save()

            #         # save new translations
            #         if translations:
            #             for translation in translations:
            #                 translation.id = None
            #                 translation.master_id = new_obj.id
            #                 translation.save()

        return government_structure

    def duplicate(self, date, with_public_servants=True):
        from ministries.models import Ministry
        from public_servants.models import PublicServant

        government_structures = GovernmentStructure.objects.filter(
            publication_date=date)
        if government_structures.exists():
            return

        government_structure = copy.copy(self)
        government_structure.id = None
        government_structure.current_government = False
        government_structure.publication_date = date
        government_structure.save()

        field_map = self._meta.fields_map

        children_government_structure = {
            'publicservant': field_map.get('publicservant'),
            'region': field_map.get('region'),
            'ministry': field_map.get('ministry'),
            'publicenterprise': field_map.get('publicenterprise'),
            'footerlink': field_map.get('footerlink'),
            'presidency': field_map.get('presidency'),
        }

        for child in children_government_structure:
            field = children_government_structure.get(child)
            print(field)

            if not field:
                continue

            if not with_public_servants:
                if field.name == 'publicservant':
                    continue

            model = field.related_model
            objects = model.objects.filter(government_structure=self)
            for obj in objects:
                new_obj = copy.copy(obj)

                # Check for and copy translations in model
                if hasattr(new_obj, 'translations'):
                    translations = copy.copy(new_obj.translations.all())
                else:
                    translations = None

                new_obj.id = None
                new_obj.government_structure = government_structure
                new_obj.save()

                if translations:
                    for translation in translations:
                        translation.id = None
                        translation.master_id = new_obj.id
                        translation.save()

                if child == 'ministry':
                    minister = PublicServant.objects.filter(
                        government_structure=government_structure
                    ).filter(name=obj.minister.name).first()
                    public_servants = PublicServant.objects.filter(
                        government_structure=government_structure,
                        name__in=obj.public_servants.values_list(
                            'name', flat=True)
                    )
                    new_obj.minister = minister
                    new_obj.public_servants.add(*public_servants)
                    new_obj.save()

                if child == 'region':
                    governor = PublicServant.objects.filter(
                        government_structure=government_structure
                    ).filter(name=obj.governor.name).first()
                    new_obj.governor = governor
                    new_obj.save()

                if child == 'publicenterprise':
                    ministries = Ministry.objects.filter(
                        government_structure=government_structure,
                    ).translated(
                        name__in=obj.ministries.values_list(
                            'translations__name', flat=True)
                    )
                    new_obj.ministries.add(*ministries)
                    new_obj.save()

                # for k, value in dict(obj._meta.fields_map).items():
                #     import ipdb
                #     ipdb.set_trace()
                #     remote_field = value.remote_field.name
                #     objs = value.related_model.objects.filter(
                #         **{remote_field: obj}
                #     )
                #     for child in objs:
                #         new_child = copy.copy(child)
                #         new_child.id = None
                #         setattr(
                #             new_child,
                #             '{}_id'.format(
                #                 remote_field,
                #             ),
                #             new_obj.id
                #         )
                #         new_child.save()

                # if not hasattr(obj, str(value.related_name)):
                #     continue

                # # if v.related_name == 'translations':
                # #     import ipdb
                # #     ipdb.set_trace()

                # for child in getattr(obj, value.related_name).all():
                #     new_child = copy.copy(child)

                #     new_child.id = None
                #     setattr(
                #         new_child,
                #         '{}_id'.format(
                #             value.remote_field.name,
                #         ),
                #         new_obj.id
                #     )
                #     new_child.save()

        return government_structure
