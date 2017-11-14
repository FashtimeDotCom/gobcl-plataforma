""" This document defines the Region app managers classes"""

from institutions.managers import InstitutionQuerySet


class CommuneQuerySet(InstitutionQuerySet):
    def by_government_structure(self, government_structure):
        qs = self
        return qs.filter(region__government_structure=government_structure)

    def with_own_municipality(self):
        return self.filter(has_own_municipality=True)

    def current_government(self):
        return self.filter(
            region__government_structure__current_government=True
        )
