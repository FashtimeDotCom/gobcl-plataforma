""" This document defines the Ministries app managers classes"""

from institutions.managers import InstitutionQuerySet


class PublicServiceQuerySet(InstitutionQuerySet):
    def by_government_structure(self, government_structure):
        qs = self
        return qs.filter(ministry__government_structure=government_structure)

    def current_government(self):
        return self.filter(
            ministry__government_structure__current_government=True
        )
