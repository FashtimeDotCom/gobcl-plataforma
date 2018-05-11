""" Small methods for generic use """

# standard library
import itertools
import os
import random
import re
import string
import unicodedata

# django
from django.apps import apps
from django.core.cache import caches
from django.utils import timezone


def today():
    """
    This method obtains today's date in local time
    """
    return timezone.localtime(timezone.now()).date()


# BROKEN
def grouper(iterable, n):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.izip_longest(
        *args
    ))


def format_rut(rut):
    if not rut:
        return ''

    rut = rut.replace(' ', '').replace('.', '').replace('-', '')
    rut = rut[:9]

    if not rut:
        return ''

    verifier = rut[-1]
    code = rut[0:-1][::-1]

    code = re.sub("(.{3})", "\\1.", code, 0, re.DOTALL)

    code = code[::-1]

    return '%s-%s' % (code, verifier)


def strip_accents(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


# BROKEN
def tz_datetime(s, *args, **kwargs):
    """
    Creates a datetime.datetime object but with the current timezone
    """
    tz = timezone.get_current_timezone()
    naive_dt = timezone.datetime(*args, **kwargs)
    return timezone.make_aware(naive_dt, tz)


def random_string(length=6, chars=None, include_spaces=True):
    if chars is None:
        chars = string.ascii_uppercase + string.digits

    if include_spaces:
        chars += ' '
    length = int(length)
    return ''.join(random.choice(chars) for x in range(length))


def get_our_models():
    for model in apps.get_models():
        app_label = model._meta.app_label

        # test only those models that we created
        if os.path.isdir(app_label):
            yield model


def can_loginas(request, target_user):
    """ This will only allow admins to log in as other users """
    return request.user.is_superuser and not target_user.is_superuser


def get_or_set_cache(name, default_callback, ttl=1800):
    """
    get a value from the cache. If not set, use the default callcabk
    Set it with a time to live that by default is ttl
    """
    cache = caches['default']
    value = cache.get(name)

    if value is None:
        value = default_callback()
        cache.set(name, value, ttl)

    return value


def keymap_replace(
        string: str,
        mappings: dict,
        lower_keys=False,
        lower_values=False,
        lower_string=False,
    ) -> str:
    """Replace parts of a string based on a dictionary.

    This function takes a string a dictionary of
    replacement mappings. For example, if I supplied
    the string "Hello world.", and the mappings
    {"H": "J", ".": "!"}, it would return "Jello world!".

    Keyword arguments:
    string       -- The string to replace characters in.
    mappings     -- A dictionary of replacement mappings.
    lower_keys   -- Whether or not to lower the keys in mappings.
    lower_values -- Whether or not to lower the values in mappings.
    lower_string -- Whether or not to lower the input string.
    """
    replaced_string = string.lower() if lower_string else string
    for character, replacement in mappings.items():
        replaced_string = replaced_string.replace(
            character.lower() if lower_keys else character,
            replacement.lower() if lower_values else replacement
        )
    return replaced_string


def remove_tags(text):
    '''
    Function to remove HTML tags
    '''
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)
