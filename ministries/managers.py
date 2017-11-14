""" This document defines the Ministries app managers classes"""

from institutions.managers import InstitutionQuerySet


class PublicServiceQuerySet(InstitutionQuerySet):
    def current_government(self):
        return self.filter(
            ministry__government_structure__current_government=True
        )
