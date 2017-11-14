""" This document defines the Region app managers classes"""

from institutions.managers import InstitutionQuerySet


class CommuneQuerySet(InstitutionQuerySet):
    def with_own_municipality(self):
        return self.filter(has_own_municipality=True)

    def current_government(self):
        return self.filter(
            region__government_structure__current_government=True
        )
