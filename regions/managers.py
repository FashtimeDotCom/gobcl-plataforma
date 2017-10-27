""" This document defines the Region app managers classes"""

from base.managers import QuerySet


class CommuneQuerySet(QuerySet):
    def with_own_municipality(self):
        return self.filter(has_own_municipality=True)
