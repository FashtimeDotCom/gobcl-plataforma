# standard library
import random
import string

# Third-party apps
from model_mommy import mommy

from phonenumber_field.modelfields import PhoneNumberField
from filer.fields.image import FilerImageField
from filer.models.imagemodels import Image

# base
from base.utils import random_string


# in the module code.path:
class CustomMommy(mommy.Mommy):

    def generate_value(self, field, commit=True):
        if field.name == 'rut':
            return '{}.{}.{}-{}'.format(
                random.randint(1, 99),
                random.randint(100, 990),
                random.randint(100, 990),
                random_string(length=1, chars='k' + string.digits),
            )
        elif isinstance(field, PhoneNumberField):
            return '+569' + str(random.randint(1, 9)) * 8
        elif isinstance(field, FilerImageField):
            return Image.objects.create()

        return super(CustomMommy, self).generate_value(field, commit)
