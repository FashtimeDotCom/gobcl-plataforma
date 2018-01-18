import inspect
from enum import Enum

from django.utils.translation import ugettext_lazy as _


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices

    @classmethod
    def get(cls, key, default=None):
        try:
            return cls[key]
        except:
            return default


class ThumbnailCropChoices(object):
    TOP_LEFT = '0,0'
    TOP_CENTER = ',0'
    TOP_RIGHT = '-0,0'

    MIDDLE_LEFT = '0,'
    MIDDLE_CENTER = ','
    MIDDLE_RIGHT = '-0,'

    BOTTOM_LEFT = '0,-0'
    BOTTOM_CENTER = ',-0'
    BOTTOM_RIGHT = '-0,-0'

    choices = (
        (TOP_LEFT, _('Top left')),
        (TOP_CENTER, _('Top center')),
        (TOP_RIGHT, _('Top right')),
        (MIDDLE_LEFT, _('Middle left')),
        (MIDDLE_CENTER, _('Middle center')),
        (MIDDLE_RIGHT, _('Middle right')),
        (BOTTOM_LEFT, _('Bottom left')),
        (BOTTOM_CENTER, _('Bottom center')),
        (BOTTOM_RIGHT, _('Bottom right')),
    )
